import pandas as pd
from sqlalchemy import create_engine
from sqlalchemy.exc import SQLAlchemyError
from .base_importer import BaseImporter
from datadashr.config import *


class SQLImporter(BaseImporter):
    def build_connection_string(self, sql_config):
        return f"{sql_config.dialect}+{sql_config.driver}://" \
               f"{sql_config.username}:{sql_config.password}@" \
               f"{sql_config.host}:{sql_config.port}/" \
               f"{sql_config.database}"

    def import_data(self, source, table_name, filters, reset):
        try:
            self._extracted_from_import_data(source, table_name, filters, reset)
        except SQLAlchemyError as e:
            logger.error(f"SQLAlchemy error: {e}")
            raise e
        except Exception as e:
            logger.error(f"Failed to import {source.source_name} of type {source.source_type}: {e}")

    # TODO Rename this here and in `import_data`
    def _extracted_from_import_data(self, source, table_name, filters, reset):
        connection_string = self.build_connection_string(source.connection_string)
        engine = create_engine(connection_string)
        query = source.query or f"SELECT * FROM {table_name.replace('_sql', '')}"

        if filters:
            filter_conditions = " AND ".join([f"{key} = '{value}'" for key, value in filters.items()])
            query += f" WHERE {filter_conditions}"

        data = pd.read_sql(query, engine)
        self.connector.import_data_into_table(data, table_name, filters, reset)
        engine.dispose()
