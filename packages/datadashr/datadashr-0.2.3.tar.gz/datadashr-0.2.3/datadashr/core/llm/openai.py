import openai
from datadashr.core.llm.base import BaseLLM
from datadashr.config import *


class OpenAILLM(BaseLLM):
    """
    OpenAILLM class for interacting with the OpenAI language models.
    """

    def __init__(self, model: str, params: dict, api_key: str, verbose: bool = False):
        """
        Constructor for OpenAILLM.

        :param model: The name of the model to use.
        :param params: Parameters for the model.
        :param api_key: The API key for authenticating with OpenAI.
        :param verbose: If True, log detailed information.
        """
        super().__init__(model, params, verbose)
        self.api_key = api_key
        openai.api_key = self.api_key

    def chat(self, messages: list) -> any:
        """
        Chat with the model.

        :param messages: A list of messages to send to the model.
        :return: The model's response as a string.
        """
        try:
            if self.verbose:
                logger.info(f"OpenAILLM messages: {messages}")
                logger.info(f"Model: {self.model}")

            response = openai.ChatCompletion.create(
                model=self.model,
                messages=messages,
                **self.params
            )

            if self.verbose:
                logger.info(f"OpenAILLM response: {response['choices'][0]['message']['content']}")

            return response['choices'][0]['message']['content']

        except Exception as e:
            if self.verbose:
                logger.error(f"OpenAILLM chat failed: {str(e)}")

            return None
