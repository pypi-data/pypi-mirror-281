from datadashr.core.pipeline.data_step import DataStep
from datadashr.config import *


class FormatContextResponseStep(DataStep):
    def __init__(self, name="FormatContextResponse"):
        super().__init__(name)

    def execute(self, context):
        try:
            llm_response = context.get('llm_response', '')
            if isinstance(llm_response, str):
                context['formatted_response'] = llm_response
            elif isinstance(llm_response, list) and len(llm_response) > 0:
                context['formatted_response'] = llm_response[0].get('content', '')
            else:
                context['formatted_response'] = 'No response from LLM.'
            logger.info(f"Formatted response: {context['formatted_response']}")
        except Exception as e:
            logger.error(f"Error in FormatContextResponseStep: {e}")
            context['formatted_response'] = 'Error formatting response.'
