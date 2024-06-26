import json
from datadashr.core.pipeline.data_step import DataStep
from datadashr.config import *


class CacheStep(DataStep):
    def execute(self, context):
        """
        Execute the cache step.
        :param context:
        :return:
        """
        try:
            request = context.get('request')
            data_connector = context.get('data_connector')
            if context.get('enable_cache'):
                self._retrieve_from_cache(context, data_connector, request)
        except Exception as e:
            if context.get('verbose'):
                logger.error(f"{self.name}: An error occurred during cache step: {e}")
            self._set_context_defaults(context)

    def _retrieve_from_cache(self, context, data_connector, request):
        """
        Retrieves the cached result if available.
        :param context:
        :param data_connector:
        :param request:
        :return:
        """
        cache_manager = context.get('cache_manager')
        tables = data_connector.existing_tables()
        table_info = data_connector.table_info()

        if cached_result := cache_manager.get(
                query=request, tables=tables, fields=table_info
        ):
            try:
                # Convert the cached result from JSON string to dictionary if it's a string
                if isinstance(cached_result, str):
                    cached_result = json.loads(cached_result)

                if not isinstance(cached_result, dict):
                    if context.get('verbose'):
                        logger.error(
                            f"{self.name}: Cached result is not in the correct format. Cache format {type(cached_result)}")
                        logger.info(f"{self.name}: Cached result: {cached_result}")
                    self._set_context_defaults(context)
                    return

                context['cached_result'] = cached_result
                context['llm_response'] = cached_result
                context['skip_prompt_generation'] = True
                if context.get('verbose'):
                    logger.info(f"{self.name}: Cache hit for request")
            except json.JSONDecodeError as e:
                if context.get('verbose'):
                    logger.error(f"{self.name}: Error decoding cached result: {e}")
                self._set_context_defaults(context)
                return
        else:
            self._set_context_defaults(context)
            if context.get('verbose'):
                logger.info(f"{self.name}: No cache hit for request")

    def _set_context_defaults(self, context):
        """
        Sets default values in the context when there is no cache hit or an error occurs.
        :param context:
        :return:
        """
        context['cached_result'] = None
        context['llm_response'] = None
        context['skip_prompt_generation'] = False
