from datadashr.config import *
from jinja2 import Environment, FileSystemLoader
from loguru import logger


class PromptManager:
    """
    Class to generate prompts for the user to solve a problem
    """

    def __init__(self, data_connector, custom_prompt: str = "", prompt_override: bool = False,
                 data_connector_type='duckdb',
                 **kwargs):
        """
        Constructor for PromptManager
        :param data:
        :param custom_prompt:
        :param prompt_override:
        :param data_connector_type:
        :param kwargs:
        """
        self.data_connector = data_connector
        self.custom_prompt = custom_prompt
        self.prompt_override = prompt_override
        self.data_connector_type = data_connector_type
        templates_path = os.path.join(os.path.dirname(__file__), 'templates', data_connector_type)
        self.env = Environment(loader=FileSystemLoader(templates_path))
        self.verbose = kwargs.get('verbose', False)

    def _existing_tables(self):
        # Estraggo tutte le tabelle e rimuovo 'relation_structure'
        existing_tables = {table[0] for table in self.data_connector.conn.execute("SHOW TABLES").fetchall()}
        existing_tables.discard('relation_structure')

        # Ottengo le tabelle inviate (che dovrebbero essere in self.data_connector.tables)
        sources = self.data_connector.tables

        # Verifico se tutte le tabelle in sources sono presenti in existing_tables
        if all(source in existing_tables for source in sources):
            if self.verbose:
                logger.info(f"return sources: {sources}")
            return set(sources)  # Restituisco solo sources
        else:
            if self.verbose:
                logger.info(f"return existing_tables: {existing_tables}")
            return existing_tables or {}

    def _table_info(self):
        table_info = {
            table: self.data_connector.conn.execute(
                f"PRAGMA table_info('{table}')"
            ).fetchdf()
            for table in self._existing_tables()
        }
        return table_info or {}

    def _relations(self):
        try:
            query = """
            SELECT source1, key1, source2, key2
            FROM relation_structure
            """
            relations_df = self.data_connector.conn.execute(query).fetchdf()
            relations = relations_df.to_dict(orient='records')
            if self.verbose:
                logger.info(f"Relations: {relations}")
            return relations or {}
        except Exception as e:
            logger.error(f"Error fetching relations: {e}")
            return {}

    def _describe_table(self):
        descriptions = self.data_connector.descriptions
        if not descriptions:
            logger.info("No descriptions available.")
        return descriptions or {}

    def build_prompt_for_role(self):
        """
        Build prompt for role
        :return:
        """
        try:
            template = self.env.get_template('role.txt')
            return template.render().strip()
        except Exception as e:
            if self.verbose:
                logger.error(f"Error building prompt for role: {e}")
            return ""

    def build_prompt(self, request):
        """
        Build prompt for DataFrame
        :param request:
        :return:
        """
        try:
            return self._extracted_from_build_prompt(request)
        except Exception as e:
            if self.verbose:
                logger.error(f"Error building prompt for DataFrame: {e}")
            return ""

    def _extracted_from_build_prompt(self, request):
        if self.prompt_override:
            return self.custom_prompt

        template = self.env.get_template('prompt.txt')
        descriptions = self._describe_table()
        table_info = self._table_info()
        relations = self._relations()
        if self.verbose:
            logger.info(f"Relations passed to template: {relations}")
        return template.render(
            descriptions=descriptions,
            table_info=table_info,
            relations=relations,
            question=request
        ).strip()

    def build_prompt_for_error_correction(self, error_message, generated_code):
        """
        Build prompt for error correction
        :param error_message:
        :param generated_code:
        :return:
        """
        try:
            template = self.env.get_template('error_correction.txt')
            return template.render(
                error_message=error_message,
                generated_code=generated_code
            ).strip()
        except Exception as e:
            if self.verbose:
                logger.error(f"Error building prompt for error correction: {e}")
            return ""
