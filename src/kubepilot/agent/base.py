"""
Base module defining the abstract interface for a kubepilot Agent.
"""

import abc
import logging
import os
from kubepilot.llm.base import LLM


class Agent(abc.ABC):
    """
    An abstract base class for various kubepilot Agents.

    Agents typically take a user query or scenario input,
    may interact with external tools (via LLM instructions),
    and produce a final response (diagnosis, plan, fix, etc.).
    """

    def __init__(self, llm: LLM):
        """
        :param llm: The LLM instance this agent uses to generate responses.
        """
        self.llm = llm
        self.logger = self.configure_logging()

    @abc.abstractmethod
    def run(self, user_input: str) -> str:
        """
        Process the user_input and return a final string (e.g., diagnosis, recommendation).
        Subclasses must implement this.
        """
        pass

    @staticmethod
    def configure_logging():
        """
        Configure logging for the agent.
        Logging behavior can be customized using environment variables:
          - AGENT_LOG_LEVEL: Log level (DEBUG, INFO, WARNING, etc.)
        """
        log_level = os.getenv("AGENT_LOG_LEVEL", "DEBUG").upper()
        log_format = "%(asctime)s [%(levelname)s] %(message)s"

        handlers = [logging.StreamHandler()]
        logging.basicConfig(level=log_level, format=log_format, handlers=handlers)
        return logging.getLogger(__name__)
