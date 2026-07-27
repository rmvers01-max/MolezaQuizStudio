from dataclasses import asdict, dataclass, field
from typing import Any


@dataclass(slots=True)
class AIContentRequest:
    tema: str
    publico: str = "Família"
    formato: str = "Vídeo longo"
    quantidade_perguntas: int = 10
    estilo: str = "Infantil, alegre e colorido"
    observacoes: str = ""
    nome_canal: str = "Moleza Quiz"

    def validar(self) -> None:
        if not self.tema.strip():
            raise ValueError("Informe o tema do conteúdo.")

        if self.quantidade_perguntas < 1 or self.quantidade_perguntas > 100:
            raise ValueError("A quantidade de perguntas deve ficar entre 1 e 100.")


@dataclass(slots=True)
class AIContentResult:
    titulo: str
    titulo_alternativo: str
    descricao: str
    hashtags: list[str] = field(default_factory=list)
    tags: list[str] = field(default_factory=list)
    texto_thumbnail: str = ""
    prompt_thumbnail: str = ""
    introducao: str = ""
    chamada_inscricao: str = ""
    perguntas: list[dict[str, Any]] = field(default_factory=list)
    observacoes_estrategicas: list[str] = field(default_factory=list)
    bruto: dict[str, Any] = field(default_factory=dict)

    def para_dict(self) -> dict[str, Any]:
        dados = asdict(self)
        dados.pop("bruto", None)
        return dados

    @classmethod
    def de_dict(cls, dados: dict[str, Any]) -> "AIContentResult":
        if not isinstance(dados, dict):
            raise ValueError("A resposta da IA não contém um objeto JSON válido.")

        hashtags = dados.get("hashtags", [])
        tags = dados.get("tags", [])
        perguntas = dados.get("perguntas", [])
        observacoes = dados.get("observacoes_estrategicas", [])

        return cls(
            titulo=str(dados.get("titulo", "")).strip(),
            titulo_alternativo=str(
                dados.get("titulo_alternativo", "")
            ).strip(),
            descricao=str(dados.get("descricao", "")).strip(),
            hashtags=[
                str(item).strip()
                for item in hashtags
                if str(item).strip()
            ] if isinstance(hashtags, list) else [],
            tags=[
                str(item).strip()
                for item in tags
                if str(item).strip()
            ] if isinstance(tags, list) else [],
            texto_thumbnail=str(
                dados.get("texto_thumbnail", "")
            ).strip(),
            prompt_thumbnail=str(
                dados.get("prompt_thumbnail", "")
            ).strip(),
            introducao=str(dados.get("introducao", "")).strip(),
            chamada_inscricao=str(
                dados.get("chamada_inscricao", "")
            ).strip(),
            perguntas=perguntas if isinstance(perguntas, list) else [],
            observacoes_estrategicas=[
                str(item).strip()
                for item in observacoes
                if str(item).strip()
            ] if isinstance(observacoes, list) else [],
            bruto=dados,
        )

    def validar(self) -> None:
        campos_obrigatorios = {
            "título": self.titulo,
            "descrição": self.descricao,
            "texto da thumbnail": self.texto_thumbnail,
            "prompt da thumbnail": self.prompt_thumbnail,
        }

        faltando = [
            nome
            for nome, valor in campos_obrigatorios.items()
            if not valor.strip()
        ]

        if faltando:
            raise ValueError(
                "A IA não preencheu: " + ", ".join(faltando) + "."
            )
