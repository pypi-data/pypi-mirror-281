import json
import datetime
from datadashr.core.pipeline.data_step import DataStep
from datadashr.config import *


class FormatResponseStep(DataStep):
    def execute(self, context):
        results = context.get('results', {})

        # Encoder personalizzato per gestire gli oggetti datetime
        def datetime_encoder(obj):
            if isinstance(obj, datetime.datetime):
                return obj.isoformat()
            raise TypeError(f"Object of type {type(obj)} is not JSON serializable")

        context['formatted_response'] = json.dumps(results, indent=4, default=datetime_encoder)
        if context.get('verbose'):
            logger.info(f"{self.name}: Formatted response {context['formatted_response']}")
