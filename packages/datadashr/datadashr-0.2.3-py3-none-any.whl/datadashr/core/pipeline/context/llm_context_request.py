from datadashr.core.pipeline.data_step import DataStep
from datadashr.config import *


class LLMContextRequestStep(DataStep):
    def __init__(self, name="LLMContextRequest"):
        super().__init__(name)

    def execute(self, context):
        try:
            llm_instance = context['llm_instance']
            prompt = context['formatted_prompt']
            response = llm_instance.chat(prompt)
            context['llm_response'] = response
            logger.info(f"LLM response: {response}")
        except Exception as e:
            logger.error(f"Error in LLMContextRequestStep: {e}")
            context['llm_response'] = []
