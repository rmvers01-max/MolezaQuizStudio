from __future__ import annotations

from .brand_profile import BrandProfile


class BrandRegistry:
    """Registro central das identidades de canal."""

    PERFIS = {
        "moleza_quiz": BrandProfile(
            nome_canal="Moleza Quiz",
            codigo="moleza_quiz",
            publico="infantil e família",
            faixa_etaria="5 a 12 anos",
            idioma="pt-BR",
            personalidade=(
                "divertido",
                "acolhedor",
                "energético",
                "positivo",
            ),
            mascote="preguiça Moleza",
            slogan="Quiz divertido para toda a família!",
            cores_principais=(
                (85, 47, 175),
                (255, 206, 56),
                (255, 104, 128),
            ),
            cores_secundarias=(
                (55, 45, 105),
                (71, 145, 245),
                (255, 255, 255),
            ),
            estilo_visual="cartoon premium vibrante",
            ritmo="dinâmico e legível",
            intensidade_visual=0.72,
            intensidade_mascote=1.0,
            frequencia_cta="moderada",
            regras={
                "abertura_max_segundos": 5.0,
                "primeira_pergunta_max_segundos": 6.0,
                "evitar_cenas_iguais_seguidas": True,
                "mascote_nunca_cobre_conteudo": True,
                "alto_contraste": True,
                "movimento_continuo_sutil": True,
                "encerramento_direciona_proximo_video": True,
            },
        ),
    }

    def obter(
        self,
        codigo="moleza_quiz",
    ) -> BrandProfile:
        return self.PERFIS.get(
            str(codigo).strip().lower(),
            self.PERFIS["moleza_quiz"],
        )
