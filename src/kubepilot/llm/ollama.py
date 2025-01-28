"""
Module for the Ollama LLM backend, interacting with a local or remote Ollama server.
"""

import json
import requests
import os
import logging
from kubepilot.llm.base import LLM

logger = logging.getLogger(__name__)


class OllamaLLM(LLM):
    """
    Example LLM that communicates with a local Ollama server (e.g., http://localhost:11434).
    """

    def __init__(self, model_name: str, base_url: str = None, api_key: str = None):
        """
        Initialize the Ollama LLM backend with a base URL and model name.
        """
        super().__init__(model_name=model_name, api_key=api_key)
        self.base_url = base_url or os.getenv("OLLAMA_URL", "http://localhost:11434")
        self.api_key = api_key or os.getenv("OLLAMA_API_KEY")

    def generate_response(self, prompt: str) -> str:
        """
        Sends the prompt to the Ollama server and returns the consolidated response.
        Handles streaming JSON responses by concatenating 'response' fields.
        """
        payload = {"prompt": prompt, "model": self.model_name}
        headers = {}

        if self.api_key:
            headers["Authorization"] = f"Bearer {self.api_key}"

        try:
            with requests.post(
                f"{self.base_url}/api/generate",
                json=payload,
                headers=headers,
                timeout=60,
                stream=True,
            ) as resp:
                resp.raise_for_status()
                full_response = ""
                for line in resp.iter_lines():
                    if line:
                        decoded_line = line.decode("utf-8")
                        try:
                            data = json.loads(decoded_line)
                            response_part = data.get("response", "")
                            full_response += response_part
                            if data.get("done", False):
                                break
                        except json.JSONDecodeError as e:
                            logger.error(
                                f"JSON decoding error: {e} - Line: {decoded_line}"
                            )
                            continue
                return full_response.strip()
        except requests.exceptions.HTTPError as http_err:
            logger.error(f"HTTP error occurred: {http_err}")
            error_response = {
                "type": "answer",
                "diagnosis": "LLM error",
                "recommendation": f"HTTP error communicating with LLM: {str(http_err)}",
            }
            return json.dumps(error_response)
        except requests.exceptions.RequestException as req_err:
            logger.error(f"Request exception: {req_err}")
            error_response = {
                "type": "answer",
                "diagnosis": "LLM error",
                "recommendation": f"Request exception communicating with LLM: {str(req_err)}",
            }
            return json.dumps(error_response)
        except Exception as generic_err:
            logger.error(f"Unexpected error: {generic_err}")
            error_response = {
                "type": "answer",
                "diagnosis": "Unexpected error",
                "recommendation": f"An unexpected error occurred: {str(generic_err)}",
            }
            return json.dumps(error_response)
