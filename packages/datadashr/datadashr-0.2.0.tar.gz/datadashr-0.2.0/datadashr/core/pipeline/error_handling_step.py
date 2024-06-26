from datadashr.core.pipeline.data_step import DataStep
from datadashr.config import *


class ErrorHandlingStep(DataStep):
    def execute(self, context):
        if invalid_queries := context.get('invalid_queries', {}):
            error_message = f"Invalid queries found: {invalid_queries}"
            context['llm_instance'].send_error_message(error_message)
            context['skip_sandbox'] = True
        if context.get('verbose'):
            logger.info(f"{self.name}: Error message sent for invalid queries")
        return