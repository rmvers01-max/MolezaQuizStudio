from pathlib import Path
import math
import struct
import wave


class SoundEffectFactory:
    TAXA_AMOSTRAGEM = 44100

    def preparar_pacote(self, pasta_projeto):
        pasta = Path(pasta_projeto) / "audios" / "efeitos"
        pasta.mkdir(parents=True, exist_ok=True)

        caminhos = {
            "entrada_a": pasta / "entrada_a.wav",
            "entrada_b": pasta / "entrada_b.wav",
            "ou": pasta / "ou.wav",
            "tick": pasta / "tick.wav",
            "tempo_esgotado": pasta / "tempo_esgotado.wav",
        }

        if not caminhos["entrada_a"].exists():
            self._gerar_tom_deslizante(
                caminhos["entrada_a"], 280, 720, 0.28
            )

        if not caminhos["entrada_b"].exists():
            self._gerar_tom_deslizante(
                caminhos["entrada_b"], 340, 820, 0.28
            )

        if not caminhos["ou"].exists():
            self._gerar_tom_curto(
                caminhos["ou"], 620, 0.18, 3
            )

        if not caminhos["tick"].exists():
            self._gerar_tom_curto(
                caminhos["tick"], 980, 0.10, 5
            )

        if not caminhos["tempo_esgotado"].exists():
            self._gerar_chime(
                caminhos["tempo_esgotado"],
                (520, 660, 820),
                0.55,
            )

        return caminhos

    def _gerar_tom_deslizante(
        self,
        caminho,
        frequencia_inicial,
        frequencia_final,
        duracao,
    ):
        total = int(self.TAXA_AMOSTRAGEM * duracao)
        amostras = []

        for indice in range(total):
            t = indice / self.TAXA_AMOSTRAGEM
            progresso = indice / max(total - 1, 1)
            frequencia = (
                frequencia_inicial
                + (frequencia_final - frequencia_inicial)
                * progresso
            )
            envelope = math.sin(math.pi * progresso) ** 1.5
            valor = (
                0.35
                * envelope
                * math.sin(2 * math.pi * frequencia * t)
            )
            amostras.append(valor)

        self._salvar_wav(caminho, amostras)

    def _gerar_tom_curto(
        self,
        caminho,
        frequencia,
        duracao,
        potencia_envelope,
    ):
        total = int(self.TAXA_AMOSTRAGEM * duracao)
        amostras = []

        for indice in range(total):
            t = indice / self.TAXA_AMOSTRAGEM
            progresso = indice / max(total - 1, 1)
            envelope = (1.0 - progresso) ** potencia_envelope
            valor = (
                0.45
                * envelope
                * math.sin(2 * math.pi * frequencia * t)
            )
            amostras.append(valor)

        self._salvar_wav(caminho, amostras)

    def _gerar_chime(
        self,
        caminho,
        frequencias,
        duracao,
    ):
        total = int(self.TAXA_AMOSTRAGEM * duracao)
        amostras = []

        for indice in range(total):
            t = indice / self.TAXA_AMOSTRAGEM
            progresso = indice / max(total - 1, 1)
            envelope = (1.0 - progresso) ** 2
            valor = 0.0

            for ordem, frequencia in enumerate(
                frequencias,
                start=1,
            ):
                valor += (
                    0.18
                    / ordem
                    * math.sin(
                        2 * math.pi * frequencia * t
                    )
                )

            amostras.append(envelope * valor)

        self._salvar_wav(caminho, amostras)

    def _salvar_wav(self, caminho, amostras):
        with wave.open(str(caminho), "w") as arquivo:
            arquivo.setnchannels(1)
            arquivo.setsampwidth(2)
            arquivo.setframerate(self.TAXA_AMOSTRAGEM)

            dados = bytearray()

            for valor in amostras:
                valor = max(-1.0, min(1.0, valor))
                dados.extend(
                    struct.pack("<h", int(valor * 32767))
                )

            arquivo.writeframes(bytes(dados))
