import pandas as pd
from .base_importer import BaseImporter
from datadashr.config import logger


class CSVImporter(BaseImporter):
    def import_data(self, source, table_name, filters, reset):
        try:
            if source.file_path:
                data = pd.read_csv(source.file_path)
                self.connector.import_data_into_table(data, table_name, filters, reset)
            else:
                raise ValueError("File path must be provided for CSV source type")
        except FileNotFoundError as e:
            logger.error(f"File not found: {e}")
        except Exception as e:
            logger.error(f"Failed to import {source.source_name} of type {source.source_type}: {e}")
