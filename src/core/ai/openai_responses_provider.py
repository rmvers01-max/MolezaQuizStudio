from .providers.openai_provider import OpenAIProvider


class OpenAIResponsesProvider(OpenAIProvider):
    """
    Nome mantido por compatibilidade com versões anteriores.
    Novos códigos devem usar AIProviderFactory ou OpenAIProvider.
    """
