from datadashr.core.pipeline.data_step import DataStep
from datadashr.config import *


class ExtractQueriesStep(DataStep):
    def execute(self, context):
        context['queries'] = context.get('llm_response', {})
        if context.get('verbose'):
            logger.info(f"{self.name}: Extracted queries {context['queries']}")
