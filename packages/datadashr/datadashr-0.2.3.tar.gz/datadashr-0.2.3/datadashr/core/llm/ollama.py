import ollama
from datadashr.core.llm.base import BaseLLM
from datadashr.config import *


class OllamaLLM(BaseLLM):
    """
    OllamaLLM class for interacting with the Ollama language model.
    """

    def __init__(self, model: str, params: dict, verbose: bool = False):
        """
        Constructor for OllamaLLM.

        :param model: The name of the model to use.
        :param params: Parameters for the model.
        :param verbose: If True, log detailed information.
        """
        super().__init__(model, params, verbose)

    def chat(self, messages: list) -> any:
        """
        Chat with the model.

        :param messages: A list of messages to send to the model.
        :return: The model's response as a string.
        """
        try:
            if self.verbose:
                logger.info(f"OllamaLLM message: {messages}")
                logger.info(f"Model: {self.model}")

            response = ollama.chat(model=self.model, messages=messages)

            if self.verbose:
                logger.info(f"OllamaLLM response: {response['message']['content']}")

            return response['message']['content']

        except Exception as e:
            if self.verbose:
                logger.error(f"OllamaLLM chat failed: {str(e)}")

            return None
