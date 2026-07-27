from .ollama_provider import OllamaProvider
from .openai_compatible_provider import OpenAICompatibleProvider
from .openai_provider import OpenAIProvider
from .simulation_provider import SimulationProvider


class AIProviderFactory:
    SIMULACAO = "Simulação (offline)"
    OPENAI = "OpenAI"
    OPENROUTER = "OpenRouter"
    OLLAMA = "Ollama"
    LM_STUDIO = "LM Studio"
    COMPATIVEL = "API compatível"

    PROVEDORES = [
        SIMULACAO,
        OPENAI,
        OPENROUTER,
        OLLAMA,
        LM_STUDIO,
        COMPATIVEL,
    ]

    @classmethod
    def criar(
        cls,
        provedor: str,
        api_key: str,
        model: str,
        base_url: str,
    ):
        nome = str(provedor).strip()

        if nome == cls.SIMULACAO:
            return SimulationProvider()

        if nome == cls.OPENAI:
            return OpenAIProvider(
                api_key=api_key,
                model=model,
                base_url=base_url or "https://api.openai.com/v1",
            )

        if nome == cls.OPENROUTER:
            return OpenAICompatibleProvider(
                api_key=api_key,
                model=model,
                base_url=base_url or "https://openrouter.ai/api/v1",
            )

        if nome == cls.OLLAMA:
            return OllamaProvider(
                model=model,
                base_url=base_url or "http://localhost:11434",
            )

        if nome == cls.LM_STUDIO:
            return OpenAICompatibleProvider(
                api_key=api_key,
                model=model,
                base_url=base_url or "http://localhost:1234/v1",
            )

        if nome == cls.COMPATIVEL:
            return OpenAICompatibleProvider(
                api_key=api_key,
                model=model,
                base_url=base_url,
            )

        raise ValueError(f"Provedor desconhecido: {nome}")
