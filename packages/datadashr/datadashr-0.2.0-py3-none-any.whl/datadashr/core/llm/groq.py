from groq import Groq
from datadashr.core.llm.base import BaseLLM
from datadashr.config import *


class GroqLLM(BaseLLM):
    """
    GroqLLM class for interacting with the Groq language models.
    """

    def __init__(self, model: str, params: dict, api_key: str = os.getenv('GROQ_API_KEY'), verbose: bool = False):
        """
        Constructor for GroqLLM.

        :param model: The name of the model to use.
        :param params: Parameters for the model.
        :param api_key: The API key for authenticating with Groq. Default is taken from environment variable.
        :param verbose: If True, log detailed information.
        """
        super().__init__(model, params, verbose)
        self.api_key = api_key or os.environ.get("GROQ_API_KEY")
        if not self.api_key:
            raise ValueError("API key must be provided either through parameter or environment variable GROQ_API_KEY")
        self.client = Groq(api_key=self.api_key)

    def chat(self, messages: list) -> any:
        """
        Chat with the model.

        :param messages: A list of messages to send to the model.
        :return: The model's response as a string.
        """
        try:
            if self.verbose:
                logger.info(f"GroqLLM messages: {messages}")
                logger.info(f"Model: {self.model}")

            chat_completion = self.client.chat.completions.create(
                messages=messages,
                model=self.model,
                **self.params
            )

            response_content = chat_completion.choices[0].message.content

            if self.verbose:
                logger.info(f"GroqLLM response: {response_content}")

            return response_content

        except Exception as e:
            if self.verbose:
                logger.error(f"GroqLLM chat failed: {str(e)}")
            return None
