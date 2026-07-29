from __future__ import annotations

from dataclasses import dataclass
import unicodedata


@dataclass(frozen=True, slots=True)
class VisualPreset:
    nome: str
    cor_fundo_inicio: tuple[int, int, int]
    cor_fundo_fim: tuple[int, int, int]
    cor_painel: tuple[int, int, int]
    paletas_perguntas: tuple[dict[str, tuple[int, int, int]], ...]
    cor_texto: tuple[int, int, int] = (255, 255, 255)
    intensidade_particulas: float = 0.45
    quantidade_confetes: int = 70
    zoom_cena: float = 1.018


class VisualPresetRegistry:
    """
    Seleciona automaticamente o estilo visual mais adequado ao tema.

    O usuário não precisa configurar cores, partículas ou animações
    pergunta por pergunta.
    """

    PRESETS = {
        "candy": VisualPreset(
            nome="Moleza Candy",
            cor_fundo_inicio=(255, 119, 176),
            cor_fundo_fim=(112, 73, 196),
            cor_painel=(70, 46, 112),
            paletas_perguntas=(
                {
                    "a": (255, 99, 145),
                    "b": (92, 158, 255),
                    "destaque": (255, 225, 92),
                },
                {
                    "a": (255, 145, 85),
                    "b": (169, 101, 255),
                    "destaque": (112, 239, 198),
                },
                {
                    "a": (237, 92, 190),
                    "b": (57, 196, 194),
                    "destaque": (255, 232, 112),
                },
            ),
            intensidade_particulas=0.55,
            quantidade_confetes=85,
            zoom_cena=1.022,
        ),
        "neon": VisualPreset(
            nome="Moleza Neon",
            cor_fundo_inicio=(38, 16, 90),
            cor_fundo_fim=(8, 12, 35),
            cor_painel=(20, 18, 48),
            paletas_perguntas=(
                {
                    "a": (255, 55, 172),
                    "b": (20, 225, 255),
                    "destaque": (255, 236, 55),
                },
                {
                    "a": (156, 58, 255),
                    "b": (16, 255, 166),
                    "destaque": (255, 116, 44),
                },
                {
                    "a": (255, 73, 91),
                    "b": (54, 129, 255),
                    "destaque": (125, 255, 78),
                },
            ),
            intensidade_particulas=0.75,
            quantidade_confetes=95,
            zoom_cena=1.025,
        ),
        "floresta": VisualPreset(
            nome="Moleza Floresta",
            cor_fundo_inicio=(44, 128, 92),
            cor_fundo_fim=(19, 58, 52),
            cor_painel=(30, 72, 59),
            paletas_perguntas=(
                {
                    "a": (110, 185, 88),
                    "b": (62, 142, 194),
                    "destaque": (255, 208, 74),
                },
                {
                    "a": (239, 140, 72),
                    "b": (77, 173, 136),
                    "destaque": (245, 225, 119),
                },
                {
                    "a": (181, 112, 72),
                    "b": (67, 155, 95),
                    "destaque": (255, 196, 74),
                },
            ),
            intensidade_particulas=0.35,
            quantidade_confetes=55,
            zoom_cena=1.015,
        ),
        "games": VisualPreset(
            nome="Moleza Games",
            cor_fundo_inicio=(41, 83, 182),
            cor_fundo_fim=(31, 22, 90),
            cor_painel=(31, 35, 84),
            paletas_perguntas=(
                {
                    "a": (255, 88, 72),
                    "b": (46, 160, 255),
                    "destaque": (255, 221, 65),
                },
                {
                    "a": (146, 75, 255),
                    "b": (30, 210, 139),
                    "destaque": (255, 132, 47),
                },
                {
                    "a": (255, 62, 147),
                    "b": (28, 190, 230),
                    "destaque": (137, 255, 86),
                },
            ),
            intensidade_particulas=0.65,
            quantidade_confetes=90,
            zoom_cena=1.023,
        ),
        "vibrante": VisualPreset(
            nome="Moleza Vibrante",
            cor_fundo_inicio=(88, 40, 170),
            cor_fundo_fim=(25, 18, 70),
            cor_painel=(35, 28, 78),
            paletas_perguntas=(
                {
                    "a": (255, 85, 115),
                    "b": (66, 145, 255),
                    "destaque": (255, 214, 75),
                },
                {
                    "a": (255, 132, 64),
                    "b": (123, 91, 255),
                    "destaque": (107, 235, 193),
                },
                {
                    "a": (233, 86, 181),
                    "b": (41, 185, 184),
                    "destaque": (255, 225, 93),
                },
                {
                    "a": (91, 175, 91),
                    "b": (255, 108, 92),
                    "destaque": (132, 188, 255),
                },
            ),
            intensidade_particulas=0.45,
            quantidade_confetes=70,
            zoom_cena=1.018,
        ),
    }

    PALAVRAS_CHAVE = {
        "candy": (
            "doce",
            "doces",
            "chocolate",
            "bolo",
            "sorvete",
            "bala",
            "sobremesa",
            "candy",
            "comida",
            "comidas",
        ),
        "neon": (
            "neon",
            "futuro",
            "futurista",
            "espaco",
            "universo",
            "galaxia",
            "robot",
            "robo",
            "tecnologia",
        ),
        "floresta": (
            "animal",
            "animais",
            "floresta",
            "natureza",
            "selva",
            "dinossauro",
            "fazenda",
            "mar",
            "oceano",
        ),
        "games": (
            "game",
            "games",
            "jogo",
            "jogos",
            "minecraft",
            "roblox",
            "fortnite",
            "videogame",
            "heroi",
            "super-heroi",
            "personagem",
        ),
    }

    def obter(
        self,
        nome: str,
    ) -> VisualPreset:
        chave = self._normalizar(nome)

        if chave in self.PRESETS:
            return self.PRESETS[chave]

        for codigo, preset in self.PRESETS.items():
            if self._normalizar(preset.nome) == chave:
                return preset

        return self.PRESETS["vibrante"]

    def selecionar_por_tema(
        self,
        tema: str,
    ) -> VisualPreset:
        texto = self._normalizar(
            tema
        )

        pontuacoes = {
            codigo: 0
            for codigo in self.PALAVRAS_CHAVE
        }

        for codigo, palavras in self.PALAVRAS_CHAVE.items():
            for palavra in palavras:
                if palavra in texto:
                    pontuacoes[codigo] += 1

        melhor = max(
            pontuacoes,
            key=pontuacoes.get,
        )

        if pontuacoes[melhor] <= 0:
            melhor = "vibrante"

        return self.PRESETS[melhor]

    def nomes_disponiveis(self) -> list[str]:
        return [
            preset.nome
            for preset in self.PRESETS.values()
        ]

    def _normalizar(
        self,
        texto: str,
    ) -> str:
        normalizado = unicodedata.normalize(
            "NFKD",
            str(texto).lower(),
        )

        sem_acentos = "".join(
            caractere
            for caractere in normalizado
            if not unicodedata.combining(
                caractere
            )
        )

        return " ".join(
            sem_acentos.split()
        )
