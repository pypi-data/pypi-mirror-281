import pyarrow.parquet as pq
from .base_importer import BaseImporter
from datadashr.config import *


class ParquetImporter(BaseImporter):
    def import_data(self, source, table_name, filters, reset):
        try:
            data = pq.read_table(source.file_path).to_pandas()
            self.connector.import_data_into_table(data, table_name, filters, reset)
        except FileNotFoundError as e:
            logger.error(f"File not found: {e}")
            raise e
        except Exception as e:
            logger.error(f"Failed to import {source.source_name} of type {source.source_type}: {e}")
            raise e
