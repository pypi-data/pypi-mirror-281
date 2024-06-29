from .base_importer import BaseImporter
from datadashr.config import *


class PolarsImporter(BaseImporter):
    def import_data(self, source, table_name, filters, reset):
        try:
            data = source.data.to_pandas()
            self.connector.import_data_into_table(data, table_name, filters, reset)
        except Exception as e:
            logger.error(f"Failed to import {source.source_name} of type {source.source_type}: {e}")
            raise e
