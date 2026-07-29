from __future__ import annotations

from dataclasses import dataclass
import unicodedata


@dataclass(frozen=True, slots=True)
class PremiumTheme:
    nome: str
    codigo: str
    familia_fonte: str
    titulo_tamanho: int
    alternativa_tamanho: int
    arredondamento_cartao: int
    particulas: str
    efeito_ambiente: str
    estilo_camera: str
    intensidade_fx: float
    intensidade_glow: float
    cor_texto: tuple[int, int, int]
    cor_secundaria: tuple[int, int, int]
    palavras_chave: tuple[str, ...]


class PremiumThemeRegistry:
    """
    Define temas completos de direção de arte.

    O tema não altera apenas cores. Ele também controla tipografia,
    arredondamento, partículas, iluminação, câmera e intensidade visual.
    """

    TEMAS = (
        PremiumTheme(
            nome="Candy Party",
            codigo="candy_party",
            familia_fonte="rounded",
            titulo_tamanho=44,
            alternativa_tamanho=29,
            arredondamento_cartao=38,
            particulas="sparkles",
            efeito_ambiente="pastel_glow",
            estilo_camera="suave",
            intensidade_fx=0.62,
            intensidade_glow=0.38,
            cor_texto=(255, 255, 255),
            cor_secundaria=(255, 230, 245),
            palavras_chave=(
                "doce",
                "doces",
                "chocolate",
                "bolo",
                "sorvete",
                "bala",
                "sobremesa",
                "comida",
                "comidas",
            ),
        ),
        PremiumTheme(
            nome="Neon Future",
            codigo="neon_future",
            familia_fonte="tech",
            titulo_tamanho=43,
            alternativa_tamanho=28,
            arredondamento_cartao=26,
            particulas="neon_dots",
            efeito_ambiente="neon_glow",
            estilo_camera="dinamica",
            intensidade_fx=0.82,
            intensidade_glow=0.68,
            cor_texto=(255, 255, 255),
            cor_secundaria=(166, 255, 244),
            palavras_chave=(
                "neon",
                "futuro",
                "futurista",
                "espaco",
                "galaxia",
                "robo",
                "robot",
                "tecnologia",
                "cyber",
            ),
        ),
        PremiumTheme(
            nome="Jungle Adventure",
            codigo="jungle_adventure",
            familia_fonte="rounded",
            titulo_tamanho=43,
            alternativa_tamanho=28,
            arredondamento_cartao=34,
            particulas="folhas",
            efeito_ambiente="green_glow",
            estilo_camera="suave",
            intensidade_fx=0.46,
            intensidade_glow=0.28,
            cor_texto=(255, 255, 255),
            cor_secundaria=(224, 255, 216),
            palavras_chave=(
                "animal",
                "animais",
                "floresta",
                "natureza",
                "selva",
                "fazenda",
                "dinossauro",
                "oceano",
                "mar",
            ),
        ),
        PremiumTheme(
            nome="Game Arena",
            codigo="game_arena",
            familia_fonte="display",
            titulo_tamanho=45,
            alternativa_tamanho=29,
            arredondamento_cartao=24,
            particulas="pixels",
            efeito_ambiente="game_glow",
            estilo_camera="dinamica",
            intensidade_fx=0.76,
            intensidade_glow=0.58,
            cor_texto=(255, 255, 255),
            cor_secundaria=(230, 240, 255),
            palavras_chave=(
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
            ),
        ),
        PremiumTheme(
            nome="Princess Dream",
            codigo="princess_dream",
            familia_fonte="elegant",
            titulo_tamanho=44,
            alternativa_tamanho=28,
            arredondamento_cartao=42,
            particulas="stars",
            efeito_ambiente="pink_glow",
            estilo_camera="suave",
            intensidade_fx=0.64,
            intensidade_glow=0.46,
            cor_texto=(255, 255, 255),
            cor_secundaria=(255, 235, 250),
            palavras_chave=(
                "princesa",
                "princesas",
                "castelo",
                "magia",
                "unicornio",
                "fada",
                "encanto",
            ),
        ),
        PremiumTheme(
            nome="Moleza Vibrante",
            codigo="moleza_vibrante",
            familia_fonte="rounded",
            titulo_tamanho=43,
            alternativa_tamanho=28,
            arredondamento_cartao=34,
            particulas="sparkles",
            efeito_ambiente="mixed_glow",
            estilo_camera="equilibrada",
            intensidade_fx=0.55,
            intensidade_glow=0.36,
            cor_texto=(255, 255, 255),
            cor_secundaria=(240, 235, 255),
            palavras_chave=(),
        ),
    )

    def selecionar(
        self,
        tema: str,
    ) -> PremiumTheme:
        texto = self._normalizar(
            tema
        )

        melhor = self.TEMAS[-1]
        melhor_pontuacao = 0

        for tema_premium in self.TEMAS:
            pontuacao = sum(
                1
                for palavra in tema_premium.palavras_chave
                if palavra in texto
            )

            if pontuacao > melhor_pontuacao:
                melhor = tema_premium
                melhor_pontuacao = pontuacao

        return melhor

    def obter(
        self,
        codigo_ou_nome: str,
    ) -> PremiumTheme:
        alvo = self._normalizar(
            codigo_ou_nome
        )

        for tema in self.TEMAS:
            if alvo in {
                self._normalizar(tema.codigo),
                self._normalizar(tema.nome),
            }:
                return tema

        return self.TEMAS[-1]

    def nomes(self) -> list[str]:
        return [
            tema.nome
            for tema in self.TEMAS
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
