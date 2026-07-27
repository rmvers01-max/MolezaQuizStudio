import math

from core.thumbnail_elements import ImageElement, ThumbnailElement


class InteractionMixin:
    def _ao_clicar(self, evento):
        elemento = self.obter_elemento_selecionado()

        if elemento is not None and not elemento.bloqueado:
            alca = self._obter_alca_no_ponto_canvas(evento.x, evento.y, elemento)

            if alca == self.ALCA_ROTACAO:
                self.girando = True
                self.arrastando = False
                self.redimensionando = False
                self.alca_ativa = alca
                self.geometria_inicial = self._capturar_geometria(elemento)
                self._preparar_rotacao(evento, elemento)
                return

            if alca is not None:
                documento_x, documento_y = self._canvas_para_documento(
                    evento.x,
                    evento.y
                )
                self.redimensionando = True
                self.arrastando = False
                self.girando = False
                self.alca_ativa = alca
                self.inicio_x_documento = documento_x
                self.inicio_y_documento = documento_y
                self.geometria_inicial = self._capturar_geometria(elemento)
                return

        documento_x, documento_y = self._canvas_para_documento(
            evento.x,
            evento.y
        )

        if not self._ponto_dentro_documento(documento_x, documento_y):
            self.selecionar_elemento(None)
            return

        elemento = self.documento.obter_elemento_no_ponto(
            documento_x,
            documento_y
        )

        if elemento is None:
            self.selecionar_elemento(None)
            return

        self.selecionar_elemento(elemento.id)

        if elemento.bloqueado:
            return

        self.arrastando = True
        self.redimensionando = False
        self.girando = False
        self.ultimo_x_documento = documento_x
        self.ultimo_y_documento = documento_y

    def _ao_arrastar(self, evento):
        elemento = self.obter_elemento_selecionado()

        if elemento is None or elemento.bloqueado:
            self.arrastando = False
            self.redimensionando = False
            self.girando = False
            return

        if self.girando:
            self._girar_elemento_com_mouse(evento, elemento)
            self.renderizar()
            return

        documento_x, documento_y = self._canvas_para_documento(
            evento.x,
            evento.y
        )

        if self.redimensionando:
            self._redimensionar_elemento_com_mouse(
                elemento,
                documento_x,
                documento_y,
                preservar_proporcao=bool(evento.state & 0x0001),
                pelo_centro=bool(evento.state & 0x0008)
            )
            self.renderizar()
            return

        if not self.arrastando:
            return

        delta_x = documento_x - self.ultimo_x_documento
        delta_y = documento_y - self.ultimo_y_documento

        elemento.deslocar(delta_x, delta_y)
        self._limitar_elemento_ao_documento(elemento)

        self.ultimo_x_documento = documento_x
        self.ultimo_y_documento = documento_y
        self.renderizar()

    def _ao_soltar(self, evento):
        houve_alteracao = (
            self.arrastando
            or self.redimensionando
            or self.girando
        )

        self.arrastando = False
        self.redimensionando = False
        self.girando = False
        self.alca_ativa = None
        self.geometria_inicial = None

        if houve_alteracao:
            self._notificar_alteracao()

        self._atualizar_cursor(evento.x, evento.y)

    def _ao_mover_mouse(self, evento):
        if self.arrastando:
            self.canvas.configure(cursor="fleur")
            return

        if self.redimensionando:
            self.canvas.configure(cursor="sizing")
            return

        if self.girando:
            self.canvas.configure(cursor="exchange")
            return

        self._atualizar_cursor(evento.x, evento.y)

    def _ao_sair_canvas(self, evento):
        if not self.arrastando and not self.redimensionando and not self.girando:
            self.canvas.configure(cursor="arrow")

    def _atualizar_cursor(self, x, y):
        elemento = self.obter_elemento_selecionado()

        if elemento is not None and not elemento.bloqueado:
            alca = self._obter_alca_no_ponto_canvas(x, y, elemento)
            if alca == self.ALCA_ROTACAO:
                self.canvas.configure(cursor="exchange")
                return
            if alca is not None:
                self.canvas.configure(cursor="sizing")
                return

        documento_x, documento_y = self._canvas_para_documento(x, y)
        elemento_no_ponto = self.documento.obter_elemento_no_ponto(
            documento_x,
            documento_y
        )

        if elemento_no_ponto is not None and not elemento_no_ponto.bloqueado:
            self.canvas.configure(cursor="fleur")
        else:
            self.canvas.configure(cursor="arrow")

    def _capturar_geometria(self, elemento):
        return {
            "x": float(elemento.x),
            "y": float(elemento.y),
            "largura": float(elemento.largura),
            "altura": float(elemento.altura),
            "rotacao": float(elemento.rotacao),
        }

    def _preparar_rotacao(self, evento, elemento):
        centro_x = elemento.x + elemento.largura / 2
        centro_y = elemento.y + elemento.altura / 2
        mouse_x, mouse_y = self._canvas_para_documento(evento.x, evento.y)
        self.angulo_mouse_inicial = math.degrees(
            math.atan2(mouse_y - centro_y, mouse_x - centro_x)
        )
        self.rotacao_inicial = float(elemento.rotacao)

    def _girar_elemento_com_mouse(self, evento, elemento):
        centro_x = elemento.x + elemento.largura / 2
        centro_y = elemento.y + elemento.altura / 2
        mouse_x, mouse_y = self._canvas_para_documento(evento.x, evento.y)
        angulo_atual = math.degrees(
            math.atan2(mouse_y - centro_y, mouse_x - centro_x)
        )
        nova_rotacao = self.rotacao_inicial + (
            angulo_atual - self.angulo_mouse_inicial
        )

        # Shift ou proximidade de 3 graus: encaixe em incrementos de 15°.
        if evento.state & 0x0001:
            nova_rotacao = round(nova_rotacao / 15) * 15
        else:
            encaixe = round(nova_rotacao / 15) * 15
            if abs(nova_rotacao - encaixe) <= 3:
                nova_rotacao = encaixe

        elemento.definir_rotacao(nova_rotacao)

    def _redimensionar_elemento_com_mouse(
        self,
        elemento: ThumbnailElement,
        documento_x: float,
        documento_y: float,
        preservar_proporcao: bool = False,
        pelo_centro: bool = False
    ):
        if self.geometria_inicial is None or self.alca_ativa is None:
            return

        g = self.geometria_inicial
        x0 = g["x"]
        y0 = g["y"]
        w0 = g["largura"]
        h0 = g["altura"]
        cx = x0 + w0 / 2
        cy = y0 + h0 / 2

        # Converte o mouse para os eixos locais do elemento.
        local_x, local_y = self._rotacionar_ponto(
            documento_x,
            documento_y,
            cx,
            cy,
            -g["rotacao"]
        )

        esquerda = x0
        topo = y0
        direita = x0 + w0
        base = y0 + h0

        alca = self.alca_ativa

        if alca in {
            self.ALCA_SUPERIOR_ESQUERDA,
            self.ALCA_MEIO_ESQUERDA,
            self.ALCA_INFERIOR_ESQUERDA,
        }:
            esquerda = local_x
        if alca in {
            self.ALCA_SUPERIOR_DIREITA,
            self.ALCA_MEIO_DIREITA,
            self.ALCA_INFERIOR_DIREITA,
        }:
            direita = local_x
        if alca in {
            self.ALCA_SUPERIOR_ESQUERDA,
            self.ALCA_MEIO_SUPERIOR,
            self.ALCA_SUPERIOR_DIREITA,
        }:
            topo = local_y
        if alca in {
            self.ALCA_INFERIOR_ESQUERDA,
            self.ALCA_MEIO_INFERIOR,
            self.ALCA_INFERIOR_DIREITA,
        }:
            base = local_y

        if pelo_centro:
            if alca in {
                self.ALCA_SUPERIOR_ESQUERDA,
                self.ALCA_MEIO_ESQUERDA,
                self.ALCA_INFERIOR_ESQUERDA,
            }:
                direita = cx + (cx - esquerda)
            elif alca in {
                self.ALCA_SUPERIOR_DIREITA,
                self.ALCA_MEIO_DIREITA,
                self.ALCA_INFERIOR_DIREITA,
            }:
                esquerda = cx - (direita - cx)

            if alca in {
                self.ALCA_SUPERIOR_ESQUERDA,
                self.ALCA_MEIO_SUPERIOR,
                self.ALCA_SUPERIOR_DIREITA,
            }:
                base = cy + (cy - topo)
            elif alca in {
                self.ALCA_INFERIOR_ESQUERDA,
                self.ALCA_MEIO_INFERIOR,
                self.ALCA_INFERIOR_DIREITA,
            }:
                topo = cy - (base - cy)

        largura = max(direita - esquerda, self.TAMANHO_MINIMO_ELEMENTO)
        altura = max(base - topo, self.TAMANHO_MINIMO_ELEMENTO)

        canto = alca in {
            self.ALCA_SUPERIOR_ESQUERDA,
            self.ALCA_SUPERIOR_DIREITA,
            self.ALCA_INFERIOR_ESQUERDA,
            self.ALCA_INFERIOR_DIREITA,
        }

        manter = preservar_proporcao or (
            isinstance(elemento, ImageElement)
            and elemento.preservar_proporcao
            and canto
        )

        if manter and h0 > 0 and canto:
            proporcao = w0 / h0
            if abs(largura - w0) >= abs(altura - h0):
                altura = largura / proporcao
            else:
                largura = altura * proporcao

            if pelo_centro:
                esquerda = cx - largura / 2
                direita = cx + largura / 2
                topo = cy - altura / 2
                base = cy + altura / 2
            else:
                if alca in {
                    self.ALCA_SUPERIOR_ESQUERDA,
                    self.ALCA_INFERIOR_ESQUERDA,
                }:
                    esquerda = direita - largura
                else:
                    direita = esquerda + largura

                if alca in {
                    self.ALCA_SUPERIOR_ESQUERDA,
                    self.ALCA_SUPERIOR_DIREITA,
                }:
                    topo = base - altura
                else:
                    base = topo + altura

        largura = max(direita - esquerda, self.TAMANHO_MINIMO_ELEMENTO)
        altura = max(base - topo, self.TAMANHO_MINIMO_ELEMENTO)

        # Centro local após a transformação, convertido de volta para o documento.
        novo_centro_local_x = esquerda + largura / 2
        novo_centro_local_y = topo + altura / 2
        novo_centro_x, novo_centro_y = self._rotacionar_ponto(
            novo_centro_local_x,
            novo_centro_local_y,
            cx,
            cy,
            g["rotacao"]
        )

        novo_x = novo_centro_x - largura / 2
        novo_y = novo_centro_y - altura / 2

        elemento.x = novo_x
        elemento.y = novo_y
        elemento.largura = largura
        elemento.altura = altura
        self._limitar_elemento_ao_documento(elemento)

    def _rotacionar_ponto(self, x, y, centro_x, centro_y, angulo):
        radianos = math.radians(angulo)
        coseno = math.cos(radianos)
        seno = math.sin(radianos)
        dx = x - centro_x
        dy = y - centro_y
        return (
            centro_x + dx * coseno - dy * seno,
            centro_y + dx * seno + dy * coseno,
        )

    def _obter_pontos_alcas_canvas(self, elemento: ThumbnailElement):
        x1, y1 = self._documento_para_canvas(elemento.x, elemento.y)
        x2, y2 = self._documento_para_canvas(
            elemento.x + elemento.largura,
            elemento.y + elemento.altura
        )
        cx = (x1 + x2) / 2
        cy = (y1 + y2) / 2

        pontos = {
            self.ALCA_SUPERIOR_ESQUERDA: (x1, y1),
            self.ALCA_MEIO_SUPERIOR: (cx, y1),
            self.ALCA_SUPERIOR_DIREITA: (x2, y1),
            self.ALCA_MEIO_ESQUERDA: (x1, cy),
            self.ALCA_MEIO_DIREITA: (x2, cy),
            self.ALCA_INFERIOR_ESQUERDA: (x1, y2),
            self.ALCA_MEIO_INFERIOR: (cx, y2),
            self.ALCA_INFERIOR_DIREITA: (x2, y2),
        }

        angulo = float(elemento.rotacao)
        if angulo:
            pontos = {
                nome: self._rotacionar_ponto(px, py, cx, cy, angulo)
                for nome, (px, py) in pontos.items()
            }

        topo_centro = pontos[self.ALCA_MEIO_SUPERIOR]
        vetor_x = topo_centro[0] - cx
        vetor_y = topo_centro[1] - cy
        comprimento = math.hypot(vetor_x, vetor_y) or 1
        distancia = 34
        pontos[self.ALCA_ROTACAO] = (
            topo_centro[0] + vetor_x / comprimento * distancia,
            topo_centro[1] + vetor_y / comprimento * distancia,
        )
        return pontos

    def _obter_alca_no_ponto_canvas(self, x, y, elemento):
        pontos = self._obter_pontos_alcas_canvas(elemento)
        area = self.AREA_CLIQUE_ALCA

        for alca, (ponto_x, ponto_y) in pontos.items():
            if abs(x - ponto_x) <= area and abs(y - ponto_y) <= area:
                return alca
        return None
