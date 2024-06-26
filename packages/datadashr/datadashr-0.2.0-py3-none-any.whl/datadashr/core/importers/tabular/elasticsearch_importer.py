import pandas as pd
from elasticsearch import Elasticsearch
from elasticsearch.helpers import scan
from .base_importer import BaseImporter
from datadashr.config import *


class ElasticsearchImporter(BaseImporter):
    def import_data(self, source, table_name, filters, reset):
        try:
            if source.username and source.password:
                es = Elasticsearch(source.host, http_auth=(source.username, source.password))
            else:
                es = Elasticsearch(source.host)
            query_body = {"query": {"match_all": {}}}  # Default query body

            if filters:
                query_body = {
                    "query": {
                        "bool": {
                            "must": [{"match": {key: value}} for key, value in filters.items()]
                        }
                    }
                }

            data = [hit["_source"] for hit in scan(es, index=source.index, query=query_body)]
            df = pd.DataFrame(data)
            self.connector.import_data_into_table(df, table_name, filters, reset)
            es.close()
        except Exception as e:
            logger.error(f"Failed to import {source.source_name} of type {source.source_type}: {e}")
            raise e
