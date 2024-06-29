from datadashr.core.pipeline.data_step import DataStep
from datadashr.config import *


class FormatContextStep(DataStep):
    def __init__(self, name="FormatContext"):
        super().__init__(name)

    def execute(self, context):
        try:
            query = context['request']
            context_text = context['retrieved_context']
            context['formatted_prompt'] = [
                {"role": "user",
                 "content": f"You are an assistant for question-answering tasks. Use the following pieces of retrieved context to answer the question. If you don't know the answer, just say that you don't know. Use three sentences maximum and keep the answer concise.Context:\n{context_text}\n\nQuestion: {query}\nAnswer:"},
            ]
            logger.info(f"Formatted prompt: {context['formatted_prompt']}")
        except Exception as e:
            logger.error(f"Error in FormatContextStep: {e}")
            context['formatted_prompt'] = []
