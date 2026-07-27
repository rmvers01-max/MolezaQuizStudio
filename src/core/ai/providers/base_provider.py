from abc import ABC, abstractmethod


class BaseAIProvider(ABC):
    """Contrato comum para provedores de texto usados pelo MolezaQuizStudio."""

    @abstractmethod
    def gerar_texto(self, prompt: str, temperatura: float = 0.7) -> str:
        raise NotImplementedError
