from datadashr.core.pipeline.data_step import DataStep
from typing import List, Dict, Tuple
from datadashr.config import *


class ExecuteQueriesStep(DataStep):
    def execute(self, context):
        queries = context.get('valid_queries', {})
        results = {'chart': [], 'table': []}

        for query_type, query_list in queries.items():
            for query in query_list:
                if context.get('verbose'):
                    logger.info(f"Executing query: {query}")
                query_results = context.get('data_connector').execute_query(query)
                if context.get('verbose'):
                    logger.info(f"Query results: {query_results}")
                parsed_results = self.parse_results(query, query_results)
                if context.get('verbose'):
                    logger.info(f"Parsed results: {parsed_results}")
                results[query_type].extend(parsed_results)

        context['results'] = results
        if context.get('verbose'):
            logger.info(f"{self.name}: Query execution results {results}")

    def parse_results(self, query: str, results: List[Tuple]) -> List[Dict[str, str]]:
        select_clause = query.split(" FROM ")[0]
        select_clause = select_clause.replace("SELECT", "").strip()
        columns = [col.strip() for col in select_clause.split(",")]

        column_names = []
        for col in columns:
            if " AS " in col:
                column_names.append(col.split(" AS ")[1].strip())
            else:
                column_name = col.split(".")[-1].strip()
                column_names.append(column_name)

        parsed_results = []
        for result in results:
            row = {column_names[i]: result[i] for i in range(len(column_names))}
            parsed_results.append(row)

        return parsed_results or []
