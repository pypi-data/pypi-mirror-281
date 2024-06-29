from datadashr.core.pipeline.data_step import DataStep
from datadashr.config import *


class RetrieveContextStep(DataStep):
    def __init__(self, name="RetrieveContext"):
        super().__init__(name)

    def execute(self, context):
        try:
            query = context['request']
            vector_instance = context['vector_instance']
            logger.info(f"Vector Instance: {vector_instance}")
            results = vector_instance.query(query)
            logger.info(f"Query Results: {results}")

            # Limitiamo il numero di documenti e la lunghezza del contesto
            max_context_length = 2000  # Limite di caratteri per il contesto
            context_text = ""
            for sublist in results['documents']:
                for doc in sublist:
                    if len(context_text) + len(doc) > max_context_length:
                        break
                    context_text += doc + "\n"
                if len(context_text) > max_context_length:
                    break

            context['retrieved_context'] = context_text
            logger.info(f"Retrieved context: {context_text}")
        except Exception as e:
            logger.error(f"Error in RetrieveContextStep: {e}")
            context['retrieved_context'] = ""
