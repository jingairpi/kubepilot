"""
Factory module for creating LLM clients based on the provider.
This allows dynamic creation of LLM clients for different backend implementations.
"""

from kubepilot.llm.ollama import OllamaLLM


def create_llm_client(provider: str, model_name: str, **kwargs):
    """
    Factory method to create an LLM client based on the provider.

    Args:
        provider (str): Name of the LLM provider (e.g., 'ollama', 'openai', 'anthropic').
        model_name (str): Name of the model to use (e.g., 'gpt-4', 'claude-v2').
        **kwargs: Additional parameters (e.g., base_url, api_key).

    Returns:
        LLM: An instance of an LLM client.

    Raises:
        ValueError: If the provider is not supported.
    """
    provider = provider.lower()

    if provider == "ollama":
        return OllamaLLM(
            model_name=model_name,
            base_url=kwargs.get("base_url"),
            api_key=kwargs.get("api_key"),
        )
    else:
        raise ValueError(f"Unsupported LLM provider: {provider}")
