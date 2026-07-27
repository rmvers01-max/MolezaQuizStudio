import asyncio
from pathlib import Path
import re

import edge_tts


class AudioGenerator:

    VOZES = {
        "Francisca — Feminina": "pt-BR-FranciscaNeural",
        "Thalita — Feminina": "pt-BR-ThalitaMultilingualNeural",
        "Antonio — Masculina": "pt-BR-AntonioNeural"
    }

    def gerar_narracoes(
        self,
        pasta_projeto,
        perguntas,
        nome_voz="Francisca — Feminina",
        velocidade="+0%",
        callback_progresso=None
    ):
        """
        Gera um arquivo MP3 para cada pergunta e resposta.

        Estrutura criada:

        audios/
            pergunta_001.mp3
            resposta_001.mp3
            pergunta_002.mp3
            resposta_002.mp3
    """

        pasta_projeto = Path(pasta_projeto)
        pasta_audios = pasta_projeto / "audios"

        pasta_audios.mkdir(
            parents=True,
            exist_ok=True
        )

        if not perguntas:
            raise ValueError(
                "O projeto não possui perguntas."
            )

        voz = self.VOZES.get(
            nome_voz,
            "pt-BR-FranciscaNeural"
        )

        asyncio.run(
            self._gerar_todos_os_audios(
                pasta_audios=pasta_audios,
                perguntas=perguntas,
                voz=voz,
                velocidade=velocidade,
                callback_progresso=callback_progresso
            )
        )

        return pasta_audios

    async def _gerar_todos_os_audios(
        self,
        pasta_audios,
        perguntas,
        voz,
        velocidade,
        callback_progresso
    ):
        total = len(perguntas)

        for numero, pergunta in enumerate(
            perguntas,
            start=1
        ):
            self._informar_progresso(
                callback_progresso,
                numero - 1,
                total,
                (
                    f"Gerando narração da pergunta "
                    f"{numero} de {total}..."
                )
            )

            texto_pergunta = self._montar_texto_pergunta(
                numero=numero,
                pergunta=pergunta
            )

            quiz_preferencia = self._eh_quiz_preferencia(
                pergunta
            )

            texto_resposta = (
                ""
                if quiz_preferencia
                else self._montar_texto_resposta(
                    pergunta
                )
            )

            texto_escolha = (
                self._montar_texto_escolha()
                if quiz_preferencia
                else ""
            )

            caminho_pergunta = (
                pasta_audios
                / f"pergunta_{numero:03d}.mp3"
            )

            caminho_resposta = (
                pasta_audios
                / f"resposta_{numero:03d}.mp3"
            )

            caminho_escolha = (
                pasta_audios
                / f"escolha_{numero:03d}.mp3"
            )

            await self._salvar_audio(
                texto=texto_pergunta,
                caminho=caminho_pergunta,
                voz=voz,
                velocidade=velocidade
            )

            if texto_resposta:
                await self._salvar_audio(
                    texto=texto_resposta,
                    caminho=caminho_resposta,
                    voz=voz,
                    velocidade=velocidade
                )

            elif caminho_resposta.exists():
                caminho_resposta.unlink()

            if texto_escolha:
                await self._salvar_audio(
                    texto=texto_escolha,
                    caminho=caminho_escolha,
                    voz=voz,
                    velocidade=velocidade
                )

            elif caminho_escolha.exists():
                caminho_escolha.unlink()

        self._informar_progresso(
            callback_progresso,
            total,
            total,
            "Narrações concluídas."
        )

    async def _salvar_audio(
        self,
        texto,
        caminho,
        voz,
        velocidade
    ):
        comunicador = edge_tts.Communicate(
            text=texto,
            voice=voz,
            rate=velocidade
        )

        await comunicador.save(
            str(caminho)
        )

    def _montar_texto_pergunta(
        self,
        numero,
        pergunta
    ):
        texto_pergunta = str(
            pergunta.get(
                "pergunta",
                "Pergunta sem texto"
            )
        ).strip()

        alternativas = pergunta.get(
            "alternativas",
            []
        )

        partes = [
            f"Pergunta número {numero}.",
            texto_pergunta
        ]

        letras_faladas = [
            "Alternativa A.",
            "Alternativa B.",
            "Alternativa C.",
            "Alternativa D."
        ]

        for indice, alternativa in enumerate(
            alternativas[:4]
        ):
            partes.append(
                (
                    f"{letras_faladas[indice]} "
                    f"{alternativa}."
                )
            )

        if self._eh_quiz_preferencia(
            pergunta
        ):
            partes.append(
                "Faça a sua escolha antes que o tempo acabe."
            )
        else:
            partes.append(
                "Qual é a resposta correta?"
            )

        return " ".join(partes)

    def _montar_texto_escolha(
        self
    ):
        return (
            "Tempo esgotado! "
            "E aí, qual você escolheu?"
        )

    def _montar_texto_resposta(
        self,
        pergunta
    ):
        resposta = self._formatar_resposta(
            pergunta
        )

        return (
            f"A resposta correta é: {resposta}. "
            "Você acertou?"
        )

    def _eh_quiz_preferencia(
        self,
        pergunta
    ) -> bool:
        tipo = str(
            pergunta.get(
                "tipo_quiz",
                ""
            )
        ).strip().lower()

        if tipo == "preferencia":
            return True

        resposta = pergunta.get(
            "resposta",
            ""
        )

        return not str(
            resposta
        ).strip()

    def _formatar_resposta(
        self,
        pergunta
    ):
        resposta = pergunta.get(
            "resposta",
            "Resposta não informada"
        )

        alternativas = pergunta.get(
            "alternativas",
            []
        )

        if isinstance(resposta, int):
            indice = resposta

            if 1 <= indice <= len(alternativas):
                indice -= 1

            if 0 <= indice < len(alternativas):
                return str(
                    alternativas[indice]
                )

        resposta_texto = str(
            resposta
        ).strip()

        resposta_limpa = re.sub(
            r"^[A-Da-d][\)\.\-\:]\s*",
            "",
            resposta_texto
        )

        if len(resposta_texto) == 1:
            letra = resposta_texto.upper()

            if letra in "ABCD":
                indice = ord(letra) - 65

                if indice < len(alternativas):
                    return str(
                        alternativas[indice]
                    )

        return resposta_limpa or resposta_texto

    def _informar_progresso(
        self,
        callback,
        atual,
        total,
        mensagem
    ):
        if callback is not None:
            callback(
                atual,
                total,
                mensagem
            )
