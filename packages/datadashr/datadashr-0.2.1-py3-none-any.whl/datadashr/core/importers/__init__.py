import duckdb
import pandas as pd
from datetime import datetime
from typing import Dict, Any, Hashable, List, Tuple
from datadashr.config import *
from datadashr.core.importers.tabular.models.import_data_config import ImportDataConfig
from datadashr.core.importers.tabular.pandas_importer import PandasImporter
from datadashr.core.importers.tabular.polars_importer import PolarsImporter
from datadashr.core.importers.tabular.csv_importer import CSVImporter
from datadashr.core.importers.tabular.sql_importer import SQLImporter
from datadashr.core.importers.tabular.elasticsearch_importer import ElasticsearchImporter
from datadashr.core.importers.tabular.parquet_importer import ParquetImporter


class Connector:
    """
    Connector Class for managing data import and interaction with DuckDB.

    External Methods:
    - connector_type(): Returns the type of the connector.
    - return_tables(): Returns the list of tables.
    - import_data(import_data, reset, reset_db): Imports data from various sources.
    - reset_database(): Resets the database, dropping all tables.
    - register_data(source_name, data): Registers a DataFrame as a table in the database.
    - define_relation(source1, key1, source2, key2): Defines a relation between two tables.
    - auto_define_relations(): Automatically defines relations based on common columns.
    - create_relation_structure_table(): Creates a table to store relations between tables.
    - execute_query(query): Executes a query and returns the results.
    - export_database(file_path): Exports the database to a specified file path.
    - get_column_types(data): Returns the column types of a DataFrame.
    - apply_filters(data, filters): Applies filters to a DataFrame.
    - import_data_into_table(data, table_name, filters, reset): Imports a DataFrame into a table.
    - existing_tables(): Returns a set of existing tables.
    - table_info(): Returns information about the existing tables.
    - get_table_description(table_name): Returns the description of a table.
    - get_all_table_descriptions(): Returns descriptions of all tables.
    - delete_table(table_name): Deletes a table from the database.
    - delete_all_tables(): Deletes all tables from the database.
    """

    IMPORTER_CLASSES = {
        'pandas': PandasImporter,
        'polars': PolarsImporter,
        'csv': CSVImporter,
        'sql': SQLImporter,
        'elasticsearch': ElasticsearchImporter,
        'parquet': ParquetImporter,
    }

    def __init__(self, db_path: str = DUCKDB_PATH, reset: bool = False, verbose: bool = False):
        """
        Initializes the Connector instance.

        Args:
            db_path (str): Path to the DuckDB database file.
            reset (bool): If True, creates an in-memory database.
            verbose (bool): If True, enables verbose logging.
        """
        if not os.path.exists(os.path.dirname(db_path)):
            os.makedirs(os.path.dirname(db_path), exist_ok=True)

        self.conn = duckdb.connect(':memory:') if reset else duckdb.connect(db_path)
        self.conn.execute("SET memory_limit = '20GB'")
        self.conn.execute("SET threads TO 5")
        self.conn.execute("SET enable_progress_bar = true")

        self.sources = {}
        self.relations = {}
        self.descriptions = {}
        self.tables = []
        self.verbose = verbose

    @staticmethod
    def connector_type():
        """
        Returns the type of the connector.

        Returns:
            str: Type of the connector ('duckdb').
        """
        return 'duckdb'

    def return_tables(self):
        """
        Returns the list of tables.

        Returns:
            List[str]: List of table names.
        """
        return self.tables

    def import_data(self, import_data: Dict[str, Any], reset: bool = False, reset_db: bool = False):
        """
        Imports data from various sources based on the provided configuration.

        Args:
            import_data (Dict[str, Any]): Configuration for data import.
            reset (bool): If True, resets the tables before importing data.
            reset_db (bool): If True, resets the entire database before importing data.
        """
        if reset_db:
            self.reset_database()

        validated_data = ImportDataConfig(**import_data)

        for source in validated_data.sources:
            source_name = source.source_name.lower()
            source_type = source.source_type
            description = source.description.lower() if source.description else "No description available"
            table_name = f"{source_name}_{source_type}" if source_type in ['polars', 'pandas', 'csv',
                                                                           'parquet'] else source_name
            if hasattr(source, 'delete_table') and source.delete_table:
                self.delete_table(table_name)

            self.tables.append(table_name)
            self.descriptions[table_name] = description
            if self.verbose:
                logger.info(f"Description {self.descriptions[table_name]} - {description}")

            if importer_class := self.IMPORTER_CLASSES.get(source_type):
                importer = importer_class(self)
                filter_conditions = source.filter
                try:
                    importer.import_data(source, table_name, filter_conditions, reset)
                except Exception as e:
                    logger.error(f"Failed to import {source_name} of type {source_type}: {e}")
            else:
                logger.error(f"Unsupported source type: {source_type}")

        if 'mapping' in import_data:
            for key, tables in import_data['mapping'].items():
                for i in range(len(tables) - 1):
                    try:
                        self.define_relation(tables[i].lower(), key.lower(), tables[i + 1].lower(), key.lower())
                    except Exception as e:
                        logger.error(f"Failed to define relation between {tables[i]} and {tables[i + 1]}: {e}")
        else:
            self.auto_define_relations()
        if self.verbose:
            logger.info(f"Relations defined before creating structure table: {self.relations}")

        self.create_relation_structure_table()

    def reset_database(self):
        """
        Resets the database by dropping all tables.
        """
        tables = self.conn.execute("SHOW TABLES").fetchall()
        for table in tables:
            self.conn.execute(f"DROP TABLE IF EXISTS {table[0]}")

        self.sources = {}
        self.relations = {}

    def register_data(self, source_name: str, data: pd.DataFrame):
        """
        Registers a DataFrame as a table in the database.

        Args:
            source_name (str): Name of the source.
            data (pd.DataFrame): Data to be registered as a table.
        """
        self.sources[source_name] = data
        if source_name in self.conn.execute("SHOW TABLES").fetchdf()['name'].str.lower().tolist():
            for d in data.itertuples(index=False):
                self.conn.execute(f"INSERT OR REPLACE INTO {source_name} VALUES {tuple(d)}")
        else:
            self.conn.execute(f"CREATE TABLE {source_name} AS SELECT * FROM data")

    def define_relation(self, source1: str, key1: str, source2: str, key2: str):
        """
        Defines a relation between two tables.

        Args:
            source1 (str): Name of the first table.
            key1 (str): Key in the first table.
            source2 (str): Name of the second table.
            key2 (str): Key in the second table.
        """
        if source1 not in self.relations:
            self.relations[source1] = []
        self.relations[source1].append((source2, key1, key2))

        if source2 not in self.relations:
            self.relations[source2] = []
        self.relations[source2].append((source1, key2, key1))
        if self.verbose:
            logger.info(
                f"Defined relation: {source1}.{key1} -> {source2}.{key2} and {source2}.{key2} -> {source1}.{key1}")

    def auto_define_relations(self):
        """
        Automatically defines relations based on common columns between tables.
        """
        source_names = list(self.sources.keys())
        for i, source1 in enumerate(source_names):
            for source2 in source_names[i + 1:]:
                columns1 = set(self.conn.execute(f"PRAGMA table_info('{source1}')").fetchdf()['name'])
                columns2 = set(self.conn.execute(f"PRAGMA table_info('{source2}')").fetchdf()['name'])
                common_keys = columns1.intersection(columns2)
                for key in common_keys:
                    try:
                        self.define_relation(source1, key, source2, key)
                    except Exception as e:
                        logger.error(f"Failed to define relation for key {key} between {source1} and {source2}: {e}")

    def create_relation_structure_table(self):
        """
        Creates a table to store relations between tables.
        """
        self.conn.execute("DROP TABLE IF EXISTS relation_structure")
        self.conn.execute(
            "CREATE TABLE relation_structure (source1 VARCHAR, key1 VARCHAR, source2 VARCHAR, key2 VARCHAR)")

        if self.verbose:
            logger.info(f"Inserting relations into relation_structure: {self.relations}")

        for source1, rels in self.relations.items():
            for (source2, key1, key2) in rels:
                try:
                    if self.verbose:
                        logger.info(f"Inserting relation: {source1}, {key1}, {source2}, {key2}")
                    self.conn.execute("INSERT INTO relation_structure VALUES (?, ?, ?, ?)",
                                      (source1, key1, source2, key2))
                except Exception as e:
                    logger.error(f"Failed to insert relation into relation_structure: {e}")

        if self.verbose:
            logger.info("Relation structure table created")
            logger.info(f"Relation structure: {self.relations}")

            relation_count = self.conn.execute("SELECT COUNT(*) FROM relation_structure").fetchone()[0]
            logger.info(f"Number of relations in relation_structure: {relation_count}")
            relations_df = self.conn.execute("SELECT * FROM relation_structure").fetchdf()
            logger.info(f"Content of relation_structure: {relations_df}")

    def execute_query(self, query: str) -> List[Tuple]:
        """
        Executes a query and returns the results.

        Args:
            query (str): SQL query to execute.

        Returns:
            List[Tuple]: Results of the query.
        """
        try:
            return self.conn.execute(query).fetchall()
        except Exception as e:
            logger.error(f"Failed to execute query: {e}")
            return []

    def export_database(self, file_path: str):
        """
        Exports the database to a specified file path.

        Args:
            file_path (str): Path to export the database.
        """
        try:
            self.conn.execute(f"EXPORT DATABASE '{file_path}'")
        except Exception as e:
            logger.error(f"Failed to export database: {e}")

    @staticmethod
    def get_column_types(data: pd.DataFrame) -> dict[Hashable, str]:
        """
        Returns the column types of a DataFrame.

        Args:
            data (pd.DataFrame): DataFrame for which to get column types.

        Returns:
            Dict[str, str]: Dictionary of column types.
        """
        column_types = {}
        for column, dtype in data.dtypes.items():
            if pd.api.types.is_integer_dtype(dtype):
                # Use BIGINT for larger integer values to avoid overflow issues
                column_types[column] = 'BIGINT' if data[column].max() > 2147483647 else 'INTEGER'
            elif pd.api.types.is_float_dtype(dtype):
                column_types[column] = 'DOUBLE'
            elif pd.api.types.is_datetime64_any_dtype(dtype):
                column_types[column] = 'TIMESTAMP'
            else:
                column_types[column] = 'VARCHAR'
        return column_types

    @staticmethod
    def apply_filters(data: pd.DataFrame, filters: Dict[str, Any]) -> pd.DataFrame:
        """
        Applies filters to a DataFrame.

        Args:
            data (pd.DataFrame): DataFrame to filter.
            filters (Dict[str, Any]): Filters to apply.

        Returns:
            pd.DataFrame: Filtered DataFrame.
        """
        for key, value in filters.items():
            data = data[data[key] == value]
        return data

    def import_data_into_table(self, data: pd.DataFrame, table_name: str, filters: Dict[str, Any], reset: bool):
        """
        Imports a DataFrame into a table.

        Args:
            data (pd.DataFrame): Data to import.
            table_name (str): Name of the table.
            filters (Dict[str, Any]): Filters to apply to the data.
            reset (bool): If True, resets the table before importing data.
        """
        try:
            data.columns = data.columns.str.lower()
            data['dt_insert'] = datetime.now()

            if filters:
                data = self.apply_filters(data, filters)

            if 'id' not in data.columns:
                data.insert(0, 'id', range(1, 1 + len(data)))

            if reset:
                self.conn.execute(f"DROP TABLE IF EXISTS {table_name}")

            column_types = self.get_column_types(data)

            if table_name in self.conn.execute("SHOW TABLES").fetchdf()['name'].str.lower().tolist():
                columns = ', '.join(data.columns)
                placeholders = ', '.join(['?'] * len(data.columns))
                insert_query = f"INSERT OR REPLACE INTO {table_name} ({columns}) VALUES ({placeholders})"
                for d in data.itertuples(index=False):
                    self.conn.execute(insert_query, tuple(d))
            else:
                columns_with_types = ', '.join([f"{col} {col_type}" for col, col_type in column_types.items()])
                create_query = f"CREATE TABLE {table_name} ({columns_with_types}, PRIMARY KEY(id))"
                self.conn.execute(create_query)
                self.conn.execute(f"INSERT INTO {table_name} SELECT * FROM data")
        except Exception as e:
            logger.error(f"Failed to import data into {table_name}: {e}")

    def existing_tables(self) -> set:
        """
        Returns a set of existing tables.

        Returns:
            set: Set of existing table names.
        """
        existing_tables = {table[0] for table in self.conn.execute("SHOW TABLES").fetchall()}
        existing_tables.discard('relation_structure')

        sources = self.tables

        if all(source in existing_tables for source in sources):
            if self.verbose:
                logger.info(f"return sources: {sources}")
            return set(sources)
        else:
            logger.info(f"return existing_tables: {existing_tables}")
            return existing_tables or set()

    def table_info(self) -> Dict[str, pd.DataFrame]:
        """
        Returns information about the existing tables.

        Returns:
            Dict[str, pd.DataFrame]: Dictionary with table names as keys and DataFrames with table information as values.
        """
        table_info = {
            table: self.conn.execute(
                f"PRAGMA table_info('{table}')"
            ).fetchdf()
            for table in self.existing_tables()
        }
        return table_info or {}

    def get_table_description(self, table_name: str) -> str:
        """
        Returns the description of a table.

        Args:
            table_name (str): Name of the table.

        Returns:
            str: Description of the table.
        """
        return self.descriptions.get(table_name, "No description available")

    def get_all_table_descriptions(self) -> Dict[str, str]:
        """
        Returns descriptions of all tables.

        Returns:
            Dict[str, str]: Dictionary with table names as keys and descriptions as values.
        """
        return self.descriptions

    def delete_table(self, table_name: str):
        """
        Deletes a table from the database.

        Args:
            table_name (str): Name of the table to delete.
        """
        try:
            self.conn.execute(f"DROP TABLE IF EXISTS {table_name}")
            if table_name in self.tables:
                self.tables.remove(table_name)
            if table_name in self.descriptions:
                del self.descriptions[table_name]
            logger.info(f"Table {table_name} deleted successfully.")
        except Exception as e:
            logger.error(f"Failed to delete table {table_name}: {e}")

    def delete_all_tables(self):
        """
        Deletes all tables from the database.
        """
        for table in self.existing_tables():
            self.delete_table(table)
        logger.info("All tables deleted successfully.")
