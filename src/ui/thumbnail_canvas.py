from typing import Callable, Optional

import customtkinter as ctk
from PIL import Image, ImageOps, ImageTk, UnidentifiedImageError

from core.thumbnail_elements import (
	ImageElement,
	ShapeElement,
	TextElement,
	ThumbnailDocument,
	ThumbnailElement
)


class ThumbnailCanvas(ctk.CTkFrame):
	"""
	Canvas visual para edição de thumbnails.

	Recursos:
	- renderização dos elementos;
	- seleção por clique;
	- movimentação com o mouse;
	- redimensionamento pelas alças dos cantos;
	- preservação da proporção de imagens;
	- indicação visual da seleção;
	- conversão entre coordenadas do editor e 1280 × 720;
	- cache de imagens usando ImageTk.PhotoImage.
	"""

	LARGURA_DOCUMENTO = 1280
	ALTURA_DOCUMENTO = 720

	TAMANHO_ALCA = 10
	AREA_CLIQUE_ALCA = 14
	TAMANHO_MINIMO_ELEMENTO = 30

	ALCA_SUPERIOR_ESQUERDA = "superior_esquerda"
	ALCA_SUPERIOR_DIREITA = "superior_direita"
	ALCA_INFERIOR_ESQUERDA = "inferior_esquerda"
	ALCA_INFERIOR_DIREITA = "inferior_direita"

	def __init__(
		self,
		master,
		largura_preview: int = 800,
		altura_preview: int = 450,
		ao_selecionar: Optional[
			Callable[[Optional[ThumbnailElement]], None]
		] = None,
		ao_alterar: Optional[
			Callable[[ThumbnailDocument], None]
		] = None
	):
		super().__init__(
			master,
			fg_color="transparent"
		)

		self.largura_preview = max(
			int(largura_preview),
			1
		)

		self.altura_preview = max(
			int(altura_preview),
			1
		)

		self.ao_selecionar = ao_selecionar
		self.ao_alterar = ao_alterar

		self.documento = ThumbnailDocument(
			largura=self.LARGURA_DOCUMENTO,
			altura=self.ALTURA_DOCUMENTO
		)

		self.elemento_selecionado_id = None

		self.arrastando = False
		self.redimensionando = False

		self.alca_ativa = None

		self.ultimo_x_documento = 0.0
		self.ultimo_y_documento = 0.0

		self.inicio_x_documento = 0.0
		self.inicio_y_documento = 0.0

		self.geometria_inicial = None

		self.escala_atual = 1.0
		self.origem_x = 0.0
		self.origem_y = 0.0

		self.imagens_cache = {}

		self._renderizacao_agendada = None

		self._criar_interface()

		self.after_idle(
			self.renderizar
		)

	def _criar_interface(self):
		self.grid_columnconfigure(
			0,
			weight=1
		)

		self.grid_rowconfigure(
			0,
			weight=1
		)

		self.canvas = ctk.CTkCanvas(
			self,
			width=self.largura_preview,
			height=self.altura_preview,
			highlightthickness=1,
			highlightbackground="#4A4A4A",
			background="#101820",
			cursor="arrow"
		)

		self.canvas.grid(
			row=0,
			column=0,
			sticky="nsew"
		)

		self.canvas.bind(
			"<Button-1>",
			self._ao_clicar
		)

		self.canvas.bind(
			"<B1-Motion>",
			self._ao_arrastar
		)

		self.canvas.bind(
			"<ButtonRelease-1>",
			self._ao_soltar
		)

		self.canvas.bind(
			"<Motion>",
			self._ao_mover_mouse
		)

		self.canvas.bind(
			"<Leave>",
			self._ao_sair_canvas
		)

		self.canvas.bind(
			"<Configure>",
			self._ao_redimensionar_canvas
		)

	# =========================================================
	# DOCUMENTO E ELEMENTOS
	# =========================================================

	def definir_documento(
		self,
		documento: ThumbnailDocument
	):
		self.documento = documento

		self.elemento_selecionado_id = None

		self.arrastando = False
		self.redimensionando = False
		self.alca_ativa = None
		self.geometria_inicial = None

		self.imagens_cache.clear()

		self.renderizar()

		self._notificar_selecao(
			None
		)

	def obter_documento(
		self
	) -> ThumbnailDocument:
		return self.documento

	def adicionar_elemento(
		self,
		elemento: ThumbnailElement
	):
		self.documento.adicionar_elemento(
			elemento
		)

		self.elemento_selecionado_id = elemento.id

		self.renderizar()

		self._notificar_selecao(
			elemento
		)

		self._notificar_alteracao()

	def remover_elemento_selecionado(
		self
	) -> bool:
		if self.elemento_selecionado_id is None:
			return False

		removido = self.documento.remover_elemento(
			self.elemento_selecionado_id
		)

		if not removido:
			return False

		self.elemento_selecionado_id = None

		self.arrastando = False
		self.redimensionando = False
		self.alca_ativa = None
		self.geometria_inicial = None

		self.renderizar()

		self._notificar_selecao(
			None
		)

		self._notificar_alteracao()

		return True

	def selecionar_elemento(
		self,
		elemento_id: Optional[str]
	):
		self.elemento_selecionado_id = elemento_id

		self.arrastando = False
		self.redimensionando = False
		self.alca_ativa = None
		self.geometria_inicial = None

		elemento = None

		if elemento_id:
			elemento = self.documento.obter_elemento(
				elemento_id
			)

		self.renderizar()

		self._notificar_selecao(
			elemento
		)

	def obter_elemento_selecionado(
		self
	) -> Optional[ThumbnailElement]:
		if not self.elemento_selecionado_id:
			return None

		return self.documento.obter_elemento(
			self.elemento_selecionado_id
		)

	def trazer_selecionado_para_frente(
		self
	):
		if not self.elemento_selecionado_id:
			return

		self.documento.trazer_para_frente(
			self.elemento_selecionado_id
		)

		self.renderizar()
		self._notificar_alteracao()

	def enviar_selecionado_para_tras(
		self
	):
		if not self.elemento_selecionado_id:
			return

		self.documento.enviar_para_tras(
			self.elemento_selecionado_id
		)

		self.renderizar()
		self._notificar_alteracao()

	# =========================================================
	# RENDERIZAÇÃO
	# =========================================================

	def renderizar(self):
		if not self.winfo_exists():
			return

		self.canvas.delete(
			"all"
		)

		largura_canvas = self.canvas.winfo_width()
		altura_canvas = self.canvas.winfo_height()

		if largura_canvas <= 1:
			largura_canvas = self.largura_preview

		if altura_canvas <= 1:
			altura_canvas = self.altura_preview

		largura_documento = max(
			int(self.documento.largura),
			1
		)

		altura_documento = max(
			int(self.documento.altura),
			1
		)

		escala = min(
			largura_canvas / largura_documento,
			altura_canvas / altura_documento
		)

		escala = max(
			escala,
			0.0001
		)

		largura_render = (
			largura_documento
			* escala
		)

		altura_render = (
			altura_documento
			* escala
		)

		origem_x = (
			largura_canvas
			- largura_render
		) / 2

		origem_y = (
			altura_canvas
			- altura_render
		) / 2

		self.escala_atual = escala
		self.origem_x = origem_x
		self.origem_y = origem_y

		self.canvas.create_rectangle(
			origem_x,
			origem_y,
			origem_x + largura_render,
			origem_y + altura_render,
			fill=self.documento.cor_fundo,
			outline="#555555",
			width=1,
			tags=("area_documento",)
		)

		elementos = sorted(
			self.documento.elementos,
			key=lambda item: item.camada
		)

		for elemento in elementos:
			if not elemento.visivel:
				continue

			try:
				self._renderizar_elemento(
					elemento
				)

			except (
				OSError,
				ValueError,
				TypeError,
				UnidentifiedImageError
			):
				self._renderizar_erro_elemento(
					elemento
				)

		elemento_selecionado = (
			self.obter_elemento_selecionado()
		)

		if elemento_selecionado:
			self._renderizar_selecao(
				elemento_selecionado
			)

	def _renderizar_elemento(
		self,
		elemento: ThumbnailElement
	):
		if isinstance(
			elemento,
			ShapeElement
		):
			self._renderizar_forma(
				elemento
			)

		elif isinstance(
			elemento,
			TextElement
		):
			self._renderizar_texto(
				elemento
			)

		elif isinstance(
			elemento,
			ImageElement
		):
			self._renderizar_imagem(
				elemento
			)

	def _renderizar_forma(
		self,
		elemento: ShapeElement
	):
		x1, y1 = self._documento_para_canvas(
			elemento.x,
			elemento.y
		)

		x2, y2 = self._documento_para_canvas(
			elemento.x + elemento.largura,
			elemento.y + elemento.altura
		)

		largura_contorno = max(
			int(
				elemento.largura_contorno
				* self.escala_atual
			),
			0
		)

		if elemento.formato == "circulo":
			self.canvas.create_oval(
				x1,
				y1,
				x2,
				y2,
				fill=elemento.cor,
				outline=(
					elemento.cor_contorno
					if largura_contorno > 0
					else ""
				),
				width=largura_contorno,
				tags=(
					"elemento",
					elemento.id
				)
			)

		else:
			self.canvas.create_rectangle(
				x1,
				y1,
				x2,
				y2,
				fill=elemento.cor,
				outline=(
					elemento.cor_contorno
					if largura_contorno > 0
					else ""
				),
				width=largura_contorno,
				tags=(
					"elemento",
					elemento.id
				)
			)

	def _renderizar_texto(
		self,
		elemento: TextElement
	):
		x1, y1 = self._documento_para_canvas(
			elemento.x,
			elemento.y
		)

		x2, y2 = self._documento_para_canvas(
			elemento.x + elemento.largura,
			elemento.y + elemento.altura
		)

		tamanho = max(
			int(
				elemento.tamanho_fonte
				* self.escala_atual
			),
			8
		)

		estilo = (
			"bold"
			if elemento.negrito
			else "normal"
		)

		fonte = (
			elemento.fonte,
			tamanho,
			estilo
		)

		ancora = "center"

		posicao_x = (
			x1 + x2
		) / 2

		if elemento.alinhamento == "esquerda":
			ancora = "w"
			posicao_x = x1

		elif elemento.alinhamento == "direita":
			ancora = "e"
			posicao_x = x2

		posicao_y = (
			y1 + y2
		) / 2

		largura_texto = max(
			int(x2 - x1),
			1
		)

		if elemento.sombra:
			self.canvas.create_text(
				posicao_x
				+ elemento.deslocamento_sombra_x
				* self.escala_atual,
				posicao_y
				+ elemento.deslocamento_sombra_y
				* self.escala_atual,
				text=elemento.texto,
				fill=elemento.cor_sombra,
				font=fonte,
				anchor=ancora,
				width=largura_texto,
				tags=(
					"elemento",
					elemento.id
				)
			)

		self.canvas.create_text(
			posicao_x,
			posicao_y,
			text=elemento.texto,
			fill=elemento.cor,
			font=fonte,
			anchor=ancora,
			width=largura_texto,
			tags=(
				"elemento",
				elemento.id
			)
		)

	def _renderizar_imagem(
		self,
		elemento: ImageElement
	):
		caminho = elemento.obter_caminho()

		x1, y1 = self._documento_para_canvas(
			elemento.x,
			elemento.y
		)

		x2, y2 = self._documento_para_canvas(
			elemento.x + elemento.largura,
			elemento.y + elemento.altura
		)

		largura_area = max(
			int(round(x2 - x1)),
			1
		)

		altura_area = max(
			int(round(y2 - y1)),
			1
		)

		if caminho is None:
			self._renderizar_placeholder_imagem(
				elemento=elemento,
				x1=x1,
				y1=y1,
				x2=x2,
				y2=y2,
				texto="Imagem não encontrada"
			)

			return

		try:
			data_modificacao = caminho.stat().st_mtime_ns

		except OSError:
			data_modificacao = 0

		chave_cache = (
			elemento.id,
			str(caminho.resolve()),
			data_modificacao,
			largura_area,
			altura_area,
			bool(elemento.preencher_area),
			bool(elemento.preservar_proporcao),
			int(elemento.opacidade)
		)

		imagem_tk = self.imagens_cache.get(
			chave_cache
		)

		if imagem_tk is None:
			try:
				with Image.open(
					caminho
				) as imagem_original:
					imagem = (
						imagem_original
						.convert("RGBA")
						.copy()
					)

			except (
				OSError,
				ValueError,
				UnidentifiedImageError
			):
				self._renderizar_placeholder_imagem(
					elemento=elemento,
					x1=x1,
					y1=y1,
					x2=x2,
					y2=y2,
					texto="Não foi possível abrir a imagem"
				)

				return

			if elemento.preencher_area:
				imagem = ImageOps.fit(
					imagem,
					(
						largura_area,
						altura_area
					),
					method=Image.Resampling.LANCZOS,
					centering=(
						0.5,
						0.5
					)
				)

			elif elemento.preservar_proporcao:
				imagem.thumbnail(
					(
						largura_area,
						altura_area
					),
					Image.Resampling.LANCZOS
				)

			else:
				imagem = imagem.resize(
					(
						largura_area,
						altura_area
					),
					Image.Resampling.LANCZOS
				)

			if imagem.width < 1 or imagem.height < 1:
				return

			if elemento.opacidade < 255:
				opacidade = max(
					min(
						int(elemento.opacidade),
						255
					),
					0
				)

				canal_alpha = imagem.getchannel(
					"A"
				)

				canal_alpha = canal_alpha.point(
					lambda valor: int(
						valor
						* (
							opacidade
							/ 255
						)
					)
				)

				imagem.putalpha(
					canal_alpha
				)

			imagem_tk = ImageTk.PhotoImage(
				imagem,
				master=self.canvas
			)

			self.imagens_cache[
				chave_cache
			] = imagem_tk

			self._limpar_cache_antigo(
				elemento.id,
				chave_cache
			)

		self.canvas.create_image(
			(
				x1 + x2
			) / 2,
			(
				y1 + y2
			) / 2,
			image=imagem_tk,
			anchor="center",
			tags=(
				"elemento",
				elemento.id
			)
		)

	def _renderizar_placeholder_imagem(
		self,
		elemento,
		x1,
		y1,
		x2,
		y2,
		texto
	):
		self.canvas.create_rectangle(
			x1,
			y1,
			x2,
			y2,
			fill="#252B35",
			outline="#777777",
			width=1,
			tags=(
				"elemento",
				elemento.id
			)
		)

		self.canvas.create_text(
			(
				x1 + x2
			) / 2,
			(
				y1 + y2
			) / 2,
			text=texto,
			fill="#CCCCCC",
			width=max(
				int(x2 - x1 - 20),
				1
			),
			justify="center",
			tags=(
				"elemento",
				elemento.id
			)
		)

	def _renderizar_erro_elemento(
		self,
		elemento
	):
		x1, y1 = self._documento_para_canvas(
			elemento.x,
			elemento.y
		)

		x2, y2 = self._documento_para_canvas(
			elemento.x + elemento.largura,
			elemento.y + elemento.altura
		)

		self.canvas.create_rectangle(
			x1,
			y1,
			x2,
			y2,
			fill="#3B2023",
			outline="#E65353",
			width=2,
			tags=(
				"elemento",
				elemento.id
			)
		)

		self.canvas.create_text(
			(
				x1 + x2
			) / 2,
			(
				y1 + y2
			) / 2,
			text="Erro ao renderizar elemento",
			fill="#FFFFFF",
			width=max(
				int(x2 - x1 - 20),
				1
			),
			tags=(
				"elemento",
				elemento.id
			)
		)

	def _limpar_cache_antigo(
		self,
		elemento_id,
		chave_atual
	):
		chaves_antigas = [
			chave
			for chave in self.imagens_cache
			if (
				chave[0] == elemento_id
				and chave != chave_atual
			)
		]

		for chave in chaves_antigas:
			self.imagens_cache.pop(
				chave,
				None
			)

	def _renderizar_selecao(
		self,
		elemento: ThumbnailElement
	):
		x1, y1 = self._documento_para_canvas(
			elemento.x,
			elemento.y
		)

		x2, y2 = self._documento_para_canvas(
			elemento.x + elemento.largura,
			elemento.y + elemento.altura
		)

		self.canvas.create_rectangle(
			x1,
			y1,
			x2,
			y2,
			outline="#36A9FF",
			width=2,
			dash=(
				6,
				4
			),
			tags=("selecao",)
		)

		pontos = self._obter_pontos_alcas_canvas(
			elemento
		)

		tamanho = self.TAMANHO_ALCA

		for alca, (
			ponto_x,
			ponto_y
		) in pontos.items():
			self.canvas.create_rectangle(
				ponto_x - tamanho / 2,
				ponto_y - tamanho / 2,
				ponto_x + tamanho / 2,
				ponto_y + tamanho / 2,
				fill="#FFFFFF",
				outline="#36A9FF",
				width=2,
				tags=(
					"selecao",
					f"alca_{alca}"
				)
			)

		if elemento.bloqueado:
			self.canvas.create_text(
				x1 + 8,
				y1 + 8,
				text="🔒",
				anchor="nw",
				fill="#FFFFFF",
				tags=("selecao",)
			)

	# =========================================================
	# MOUSE
	# =========================================================

	def _ao_clicar(
		self,
		evento
	):
		elemento_selecionado = (
			self.obter_elemento_selecionado()
		)

		if (
			elemento_selecionado is not None
			and not elemento_selecionado.bloqueado
		):
			alca = self._obter_alca_no_ponto_canvas(
				evento.x,
				evento.y,
				elemento_selecionado
			)

			if alca is not None:
				documento_x, documento_y = (
					self._canvas_para_documento(
						evento.x,
						evento.y
					)
				)

				self.redimensionando = True
				self.arrastando = False

				self.alca_ativa = alca

				self.inicio_x_documento = documento_x
				self.inicio_y_documento = documento_y

				self.geometria_inicial = {
					"x": elemento_selecionado.x,
					"y": elemento_selecionado.y,
					"largura": elemento_selecionado.largura,
					"altura": elemento_selecionado.altura
				}

				return

		documento_x, documento_y = (
			self._canvas_para_documento(
				evento.x,
				evento.y
			)
		)

		if not self._ponto_dentro_documento(
			documento_x,
			documento_y
		):
			self.selecionar_elemento(
				None
			)

			return

		elemento = (
			self.documento
			.obter_elemento_no_ponto(
				documento_x,
				documento_y
			)
		)

		if elemento is None:
			self.selecionar_elemento(
				None
			)

			return

		self.selecionar_elemento(
			elemento.id
		)

		if elemento.bloqueado:
			return

		self.arrastando = True
		self.redimensionando = False

		self.ultimo_x_documento = documento_x
		self.ultimo_y_documento = documento_y

	def _ao_arrastar(
		self,
		evento
	):
		elemento = (
			self.obter_elemento_selecionado()
		)

		if elemento is None or elemento.bloqueado:
			self.arrastando = False
			self.redimensionando = False
			return

		documento_x, documento_y = (
			self._canvas_para_documento(
				evento.x,
				evento.y
			)
		)

		if self.redimensionando:
			self._redimensionar_elemento_com_mouse(
				elemento=elemento,
				documento_x=documento_x,
				documento_y=documento_y
			)

			self.renderizar()
			return

		if not self.arrastando:
			return

		delta_x = (
			documento_x
			- self.ultimo_x_documento
		)

		delta_y = (
			documento_y
			- self.ultimo_y_documento
		)

		elemento.deslocar(
			delta_x,
			delta_y
		)

		self._limitar_elemento_ao_documento(
			elemento
		)

		self.ultimo_x_documento = documento_x
		self.ultimo_y_documento = documento_y

		self.renderizar()

	def _ao_soltar(
		self,
		evento
	):
		houve_alteracao = (
			self.arrastando
			or self.redimensionando
		)

		self.arrastando = False
		self.redimensionando = False

		self.alca_ativa = None
		self.geometria_inicial = None

		if houve_alteracao:
			self._notificar_alteracao()

		self._atualizar_cursor(
			evento.x,
			evento.y
		)

	def _ao_mover_mouse(
		self,
		evento
	):
		if self.arrastando:
			self.canvas.configure(
				cursor="fleur"
			)
			return

		if self.redimensionando:
			self.canvas.configure(
				cursor="sizing"
			)
			return

		self._atualizar_cursor(
			evento.x,
			evento.y
		)

	def _ao_sair_canvas(
		self,
		evento
	):
		if not self.arrastando and not self.redimensionando:
			self.canvas.configure(
				cursor="arrow"
			)

	def _atualizar_cursor(
		self,
		x,
		y
	):
		elemento = (
			self.obter_elemento_selecionado()
		)

		if (
			elemento is not None
			and not elemento.bloqueado
		):
			alca = self._obter_alca_no_ponto_canvas(
				x,
				y,
				elemento
			)

			if alca is not None:
				self.canvas.configure(
					cursor="sizing"
				)
				return

		documento_x, documento_y = (
			self._canvas_para_documento(
				x,
				y
			)
		)

		elemento_no_ponto = (
			self.documento
			.obter_elemento_no_ponto(
				documento_x,
				documento_y
			)
		)

		if (
			elemento_no_ponto is not None
			and not elemento_no_ponto.bloqueado
		):
			self.canvas.configure(
				cursor="fleur"
			)
		else:
			self.canvas.configure(
				cursor="arrow"
			)

	# =========================================================
	# REDIMENSIONAMENTO
	# =========================================================

	def _redimensionar_elemento_com_mouse(
		self,
		elemento: ThumbnailElement,
		documento_x: float,
		documento_y: float
	):
		if (
			self.geometria_inicial is None
			or self.alca_ativa is None
		):
			return

		inicial_x = self.geometria_inicial["x"]
		inicial_y = self.geometria_inicial["y"]

		inicial_largura = (
			self.geometria_inicial["largura"]
		)

		inicial_altura = (
			self.geometria_inicial["altura"]
		)

		direita_inicial = (
			inicial_x
			+ inicial_largura
		)

		base_inicial = (
			inicial_y
			+ inicial_altura
		)

		novo_x = inicial_x
		novo_y = inicial_y
		nova_largura = inicial_largura
		nova_altura = inicial_altura

		if self.alca_ativa == self.ALCA_SUPERIOR_ESQUERDA:
			novo_x = documento_x
			novo_y = documento_y

			nova_largura = (
				direita_inicial
				- novo_x
			)

			nova_altura = (
				base_inicial
				- novo_y
			)

		elif self.alca_ativa == self.ALCA_SUPERIOR_DIREITA:
			novo_y = documento_y

			nova_largura = (
				documento_x
				- inicial_x
			)

			nova_altura = (
				base_inicial
				- novo_y
			)

		elif self.alca_ativa == self.ALCA_INFERIOR_ESQUERDA:
			novo_x = documento_x

			nova_largura = (
				direita_inicial
				- novo_x
			)

			nova_altura = (
				documento_y
				- inicial_y
			)

		elif self.alca_ativa == self.ALCA_INFERIOR_DIREITA:
			nova_largura = (
				documento_x
				- inicial_x
			)

			nova_altura = (
				documento_y
				- inicial_y
			)

		nova_largura = max(
			nova_largura,
			self.TAMANHO_MINIMO_ELEMENTO
		)

		nova_altura = max(
			nova_altura,
			self.TAMANHO_MINIMO_ELEMENTO
		)

		preservar_proporcao = (
			isinstance(
				elemento,
				ImageElement
			)
			and elemento.preservar_proporcao
			and inicial_altura > 0
		)

		if preservar_proporcao:
			proporcao = (
				inicial_largura
				/ inicial_altura
			)

			delta_largura = abs(
				nova_largura
				- inicial_largura
			)

			delta_altura = abs(
				nova_altura
				- inicial_altura
			)

			if delta_largura >= delta_altura:
				nova_altura = (
					nova_largura
					/ proporcao
				)
			else:
				nova_largura = (
					nova_altura
					* proporcao
				)

			if self.alca_ativa in {
				self.ALCA_SUPERIOR_ESQUERDA,
				self.ALCA_INFERIOR_ESQUERDA
			}:
				novo_x = (
					direita_inicial
					- nova_largura
				)

			if self.alca_ativa in {
				self.ALCA_SUPERIOR_ESQUERDA,
				self.ALCA_SUPERIOR_DIREITA
			}:
				novo_y = (
					base_inicial
					- nova_altura
				)

		novo_x, novo_y, nova_largura, nova_altura = (
			self._limitar_redimensionamento(
				x=novo_x,
				y=novo_y,
				largura=nova_largura,
				altura=nova_altura,
				alca=self.alca_ativa,
				direita_inicial=direita_inicial,
				base_inicial=base_inicial
			)
		)

		elemento.x = novo_x
		elemento.y = novo_y

		elemento.largura = max(
			nova_largura,
			self.TAMANHO_MINIMO_ELEMENTO
		)

		elemento.altura = max(
			nova_altura,
			self.TAMANHO_MINIMO_ELEMENTO
		)

	def _limitar_redimensionamento(
		self,
		x,
		y,
		largura,
		altura,
		alca,
		direita_inicial,
		base_inicial
	):
		largura_documento = (
			self.documento.largura
		)

		altura_documento = (
			self.documento.altura
		)

		if x < 0:
			x = 0

			if alca in {
				self.ALCA_SUPERIOR_ESQUERDA,
				self.ALCA_INFERIOR_ESQUERDA
			}:
				largura = direita_inicial

		if y < 0:
			y = 0

			if alca in {
				self.ALCA_SUPERIOR_ESQUERDA,
				self.ALCA_SUPERIOR_DIREITA
			}:
				altura = base_inicial

		if x + largura > largura_documento:
			largura = max(
				largura_documento - x,
				self.TAMANHO_MINIMO_ELEMENTO
			)

		if y + altura > altura_documento:
			altura = max(
				altura_documento - y,
				self.TAMANHO_MINIMO_ELEMENTO
			)

		largura = max(
			largura,
			self.TAMANHO_MINIMO_ELEMENTO
		)

		altura = max(
			altura,
			self.TAMANHO_MINIMO_ELEMENTO
		)

		return (
			x,
			y,
			largura,
			altura
		)

	def _obter_pontos_alcas_canvas(
		self,
		elemento: ThumbnailElement
	):
		x1, y1 = self._documento_para_canvas(
			elemento.x,
			elemento.y
		)

		x2, y2 = self._documento_para_canvas(
			elemento.x + elemento.largura,
			elemento.y + elemento.altura
		)

		return {
			self.ALCA_SUPERIOR_ESQUERDA: (
				x1,
				y1
			),
			self.ALCA_SUPERIOR_DIREITA: (
				x2,
				y1
			),
			self.ALCA_INFERIOR_ESQUERDA: (
				x1,
				y2
			),
			self.ALCA_INFERIOR_DIREITA: (
				x2,
				y2
			)
		}

	def _obter_alca_no_ponto_canvas(
		self,
		x,
		y,
		elemento
	):
		pontos = self._obter_pontos_alcas_canvas(
			elemento
		)

		area = self.AREA_CLIQUE_ALCA

		for alca, (
			ponto_x,
			ponto_y
		) in pontos.items():
			if (
				abs(x - ponto_x) <= area
				and abs(y - ponto_y) <= area
			):
				return alca

		return None

	# =========================================================
	# REDIMENSIONAMENTO DO CANVAS
	# =========================================================

	def _ao_redimensionar_canvas(
		self,
		evento
	):
		if self._renderizacao_agendada is not None:
			try:
				self.after_cancel(
					self._renderizacao_agendada
				)

			except ValueError:
				pass

		self._renderizacao_agendada = self.after(
			40,
			self._renderizar_apos_redimensionamento
		)

	def _renderizar_apos_redimensionamento(
		self
	):
		self._renderizacao_agendada = None
		self.renderizar()

	# =========================================================
	# CONVERSÕES E LIMITES
	# =========================================================

	def _limitar_elemento_ao_documento(
		self,
		elemento: ThumbnailElement
	):
		largura_maxima = max(
			self.documento.largura
			- elemento.largura,
			0
		)

		altura_maxima = max(
			self.documento.altura
			- elemento.altura,
			0
		)

		elemento.x = max(
			min(
				elemento.x,
				largura_maxima
			),
			0
		)

		elemento.y = max(
			min(
				elemento.y,
				altura_maxima
			),
			0
		)

	def _documento_para_canvas(
		self,
		x: float,
		y: float
	) -> tuple[float, float]:
		return (
			self.origem_x
			+ x
			* self.escala_atual,
			self.origem_y
			+ y
			* self.escala_atual
		)

	def _canvas_para_documento(
		self,
		x: float,
		y: float
	) -> tuple[float, float]:
		escala = max(
			self.escala_atual,
			0.0001
		)

		return (
			(
				x
				- self.origem_x
			)
			/ escala,
			(
				y
				- self.origem_y
			)
			/ escala
		)

	def _ponto_dentro_documento(
		self,
		x,
		y
	):
		return (
			0 <= x <= self.documento.largura
			and 0 <= y <= self.documento.altura
		)

	# =========================================================
	# NOTIFICAÇÕES
	# =========================================================

	def _notificar_selecao(
		self,
		elemento: Optional[ThumbnailElement]
	):
		if callable(
			self.ao_selecionar
		):
			self.ao_selecionar(
				elemento
			)

	def _notificar_alteracao(
		self
	):
		if callable(
			self.ao_alterar
		):
			self.ao_alterar(
				self.documento
			)

