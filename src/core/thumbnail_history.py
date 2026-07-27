from copy import deepcopy
from typing import Optional

from core.thumbnail_elements import ThumbnailDocument


class ThumbnailHistory:
	"""
	Gerencia o histórico de alterações do Editor de Thumbnail.

	Cada estado armazenado é uma cópia independente do documento,
	permitindo desfazer e refazer alterações sem modificar os estados
	anteriores.

	O histórico possui um limite para evitar consumo excessivo de memória.
	"""

	def __init__(
		self,
		limite: int = 50
	):
		self.limite = max(
			int(limite),
			2
		)

		self.estados: list[ThumbnailDocument] = []
		self.indice_atual = -1

		self.restaurando_estado = False

	def iniciar(
		self,
		documento: ThumbnailDocument
	):
		"""
		Limpa o histórico e registra o documento como estado inicial.
		"""

		self.estados.clear()
		self.indice_atual = -1

		self.registrar(
			documento
		)

	def registrar(
		self,
		documento: ThumbnailDocument
	) -> bool:
		"""
		Registra uma cópia do documento.

		Caso o usuário tenha desfeito alterações e depois realize uma
		modificação nova, os estados de refazer são descartados.
		"""

		if self.restaurando_estado:
			return False

		copia_documento = deepcopy(
			documento
		)

		if self._estado_igual_ao_atual(
			copia_documento
		):
			return False

		if self.indice_atual < len(self.estados) - 1:
			self.estados = self.estados[
				:self.indice_atual + 1
			]

		self.estados.append(
			copia_documento
		)

		self.indice_atual = len(
			self.estados
		) - 1

		self._aplicar_limite()

		return True

	def pode_desfazer(
		self
	) -> bool:
		return (
			len(self.estados) > 1
			and self.indice_atual > 0
		)

	def pode_refazer(
		self
	) -> bool:
		return (
			self.indice_atual >= 0
			and self.indice_atual
			< len(self.estados) - 1
		)

	def desfazer(
		self
	) -> Optional[ThumbnailDocument]:
		if not self.pode_desfazer():
			return None

		self.indice_atual -= 1

		return self._obter_copia_estado_atual()

	def refazer(
		self
	) -> Optional[ThumbnailDocument]:
		if not self.pode_refazer():
			return None

		self.indice_atual += 1

		return self._obter_copia_estado_atual()

	def obter_estado_atual(
		self
	) -> Optional[ThumbnailDocument]:
		return self._obter_copia_estado_atual()

	def quantidade_estados(
		self
	) -> int:
		return len(
			self.estados
		)

	def limpar(
		self
	):
		self.estados.clear()
		self.indice_atual = -1
		self.restaurando_estado = False

	def iniciar_restauracao(
		self
	):
		"""
		Impede que a aplicação de um estado restaurado seja registrada
		novamente como uma alteração nova.
		"""

		self.restaurando_estado = True

	def finalizar_restauracao(
		self
	):
		self.restaurando_estado = False

	def _obter_copia_estado_atual(
		self
	) -> Optional[ThumbnailDocument]:
		if (
			self.indice_atual < 0
			or self.indice_atual >= len(self.estados)
		):
			return None

		return deepcopy(
			self.estados[
				self.indice_atual
			]
		)

	def _estado_igual_ao_atual(
		self,
		documento: ThumbnailDocument
	) -> bool:
		if (
			self.indice_atual < 0
			or self.indice_atual >= len(self.estados)
		):
			return False

		estado_atual = self.estados[
			self.indice_atual
		]

		return (
			estado_atual.para_dict()
			== documento.para_dict()
		)

	def _aplicar_limite(
		self
	):
		excesso = (
			len(self.estados)
			- self.limite
		)

		if excesso <= 0:
			return

		self.estados = self.estados[
			excesso:
		]

		self.indice_atual = max(
			self.indice_atual - excesso,
			0
		)

