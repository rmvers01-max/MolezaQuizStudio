from .base_template import BaseVideoTemplate


class PreferenceVideoTemplate(BaseVideoTemplate):
    tipo_quiz = "preferencia"
    nome = "O que você prefere?"

    def texto_encerramento_padrao(self) -> str:
        return (
            "Qual foi a sua escolha favorita? "
            "Conte nos comentários!"
        )
