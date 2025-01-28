"""
Base module for defining the abstract interface for Large Language Model (LLM) backends.
"""

import abc


class LLM(abc.ABC):
    """
    An abstract base class defining the interface for LLM backends.
    """

    # pylint: disable=too-few-public-methods

    def __init__(self, model_name: str, api_key: str = None):
        """
        Initialize the LLM backend with a model name and optional API key.
        """
        self.model_name = model_name
        self.api_key = api_key

    @abc.abstractmethod
    def generate_response(self, prompt: str) -> str:
        """
        Generate a textual response for the given prompt.
        Subclasses must implement this.
        """
        pass
