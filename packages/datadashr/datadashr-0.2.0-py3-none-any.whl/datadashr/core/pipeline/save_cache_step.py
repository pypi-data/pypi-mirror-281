from datadashr.core.pipeline.data_step import DataStep
from datadashr.config import *


class SaveCacheStep(DataStep):
    def execute(self, context):
        """
        Execute the save cache step.
        :param context:
        :return:
        """
        try:
            request = context.get('request')
            data_connector = context.get('data_connector')
            if context.get('enable_cache'):
                self._save_to_cache(context, data_connector, request)
        except Exception as e:
            if context.get('verbose'):
                logger.error(f"{self.name}: An error occurred during cache saving: {e}")
            return

    def _save_to_cache(self, context, data_connector, request):
        """
        Saves the current state to the cache.
        :param context:
        :param data_connector:
        :param request:
        :return:
        """
        cache_manager = context.get('cache_manager')
        tables = data_connector.existing_tables()
        table_info = data_connector.table_info()
        llm_response = context.get('llm_response')

        if not isinstance(llm_response, dict):
            if context.get('verbose'):
                logger.error(f"{self.name}: llm_response is not in the correct format.")
            return

        cache_manager.set(
            query=request,
            tables=tables,
            fields=table_info,
            response=llm_response,
        )
        if context.get('verbose'):
            logger.info(f"{self.name}: Cache saved for request")
