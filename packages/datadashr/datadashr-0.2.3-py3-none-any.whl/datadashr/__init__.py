"""
DataDashr: An Advanced Data Interaction Pipeline

Overview:
DataDashr is a comprehensive pipeline designed to facilitate data interaction through a combination of large language models (LLMs), data importers, caching, and query execution. This pipeline automates the processing of requests, managing data, generating prompts, and executing queries to return formatted responses. It is highly customizable and supports logging for detailed tracking of operations.

Classes and Methods:

1. DataDashr:
    - __init__(self, llm_instance: BaseLLM, data, **kwargs):
        Initializes the DataDashr pipeline with the necessary components including the LLM instance, data connector, cache manager, vector manager, and prompt manager. Sets up directories for caching, vectors, charts, and logs.
        - Parameters:
            - llm_instance: Instance of BaseLLM for processing natural language requests.
            - data: Initial data to be imported via the data connector.
            - kwargs: Optional arguments to customize the behavior and settings of the pipeline.
        - Attributes:
            - llm_instance: Stores the LLM instance.
            - data_connector: Manages the connection to the data source.
            - path: Path to the current directory or specified in kwargs.
            - data_connector_type: Type of data connector used.
            - cache_dir, chart_dir, log_dir, db_path: Directories for storing cache, vectors, charts, logs, and database path.
            - logger: Logger instance for recording pipeline activities.
            - cache_manager: Manages caching operations.
            - prompt_manager: Manages prompt generation based on the data connector and custom settings.
            - ut: Utilities instance for additional operations.
            - enable_cache: Flag to enable or disable caching.
            - format_type: Specifies the format of the response (default is 'api').
            - request: Stores the current request being processed.

    - chat(self, request):
        Executes the data processing pipeline for a given request. It goes through several steps including caching, prompt generation, LLM request, query extraction, validation, execution, error handling, and formatting the response.
        - Parameters:
            - request: The request to be processed by the pipeline.
        - Returns:
            - The formatted response from the LLM or an error message if no response is available.
"""
import random
from datadashr.core.llm.base import BaseLLM
from datadashr.core.utilities.cache import CacheManager
from datadashr.core.prompt import PromptManager
from datadashr.core.utilities import Utilities
from datadashr.core.pipeline import Pipeline, CacheStep, PromptGenerationStep, LLMRequestStep, ErrorHandlingStep, \
    FormatResponseStep, SaveCacheStep, ExtractQueriesStep, ExecuteQueriesStep, ValidateQueriesStep, \
    FormatContextResponseStep, LLMContextRequestStep, FormatContextStep, RetrieveContextStep
from datadashr.core.importers import Connector
from datadashr.core.importers.vector.datadashr_vector import DatadashrDBVector
from jinja2 import Environment, FileSystemLoader
from datadashr.config import *


class DataDashr:
    def __init__(self, llm_instance: BaseLLM, data, **kwargs):
        self.llm_instance = llm_instance
        self.data_connector = Connector()
        self.path = kwargs.get('path', os.path.dirname(os.path.realpath(__file__)))
        self.data_connector_type = self.data_connector.connector_type()
        self.cache_dir = CACHE_DIR
        self.chart_dir = CHART_DIR
        self.log_dir = LOG_DIR
        self.db_path = DUCKDB_PATH
        self.logger = LogManager(self.log_dir)
        os.makedirs(self.cache_dir, exist_ok=True)
        self.verbose = kwargs.get('verbose', False)
        self.reset_db = self.reset_cache = kwargs.get('reset_db', False)
        self.cache_manager = CacheManager(self.cache_dir, self.reset_cache, self.verbose)

        self.ut = Utilities(self.verbose)
        self.enable_cache = kwargs.get('enable_cache', False)
        self.format_type = kwargs.get('format_type', 'api')
        self.reset_collection = kwargs.get('reset_collection', False)
        self.overwrite_file = kwargs.get('overwrite_file', False)

        self.data_connector.import_data(data, reset=self.reset_db)

        self.request = None
        self.env = Environment(loader=FileSystemLoader(FANCY_RESPONSE_TEMPLATE))

        self.prompt_manager = PromptManager(data_connector=self.data_connector,
                                            custom_prompt=kwargs.get('custom_prompt', ""),
                                            prompt_override=kwargs.get('prompt_override', False),
                                            data_connector_type=self.data_connector_type,
                                            verbose=self.verbose)
        self.embedding_manager = DatadashrDBVector(db_path=VECTOR_DIR, collection_name='datadashr',
                                                   embedding_type='ollama',
                                                   embedding_model='nomic-embed-text:latest',
                                                   embedding_key=None,
                                                   reset_collection=self.reset_collection,
                                                   overwrite_file=self.overwrite_file)

    def chat(self, request, response_mode='data'):
        if self.verbose:
            logger.info(f"Executing pipeline for request: {request}")
        self.request = request

        # Load responses template
        template = self.env.get_template('fancy_response.txt')
        response_text = template.render(request=request)
        responses = response_text.splitlines()
        logger.info(random.choice(responses))

        context = {
            'llm_instance': self.llm_instance,
            'data_connector': self.data_connector,
            'cache_manager': self.cache_manager,
            'prompt_manager': self.prompt_manager,
            'vector_instance': self.embedding_manager,
            'utilities': self.ut,
            'request': request,
            'enable_cache': self.enable_cache,
            'format_type': self.format_type,
            'chart_dir': self.chart_dir,
            'data_connector_type': self.data_connector_type,
            'verbose': self.verbose,
        }

        step = Pipeline(**context)

        if response_mode == 'data':
            step.add_step(
                CacheStep("Cache") |
                PromptGenerationStep("PromptGeneration") |
                LLMRequestStep("LLMRequest") |
                ExtractQueriesStep("ExtractQueries") |
                ValidateQueriesStep("ValidateQueries") |
                ErrorHandlingStep("ErrorHandling") |
                ExecuteQueriesStep("ExecuteQueries") |
                FormatResponseStep("FormatResponse") |
                SaveCacheStep("SaveCache")
            )

        elif response_mode == 'context':

            step.add_step(
                RetrieveContextStep("RetrieveContext") |
                FormatContextStep("FormatContext") |
                LLMContextRequestStep("LLMContextRequest") |
                FormatContextResponseStep("FormatContextResponse")
            )

        final_context = step.run()
        if self.verbose:
            logger.info(f"Final context: {final_context}")

        formatted_response = final_context.get('formatted_response')
        if self.verbose:
            logger.info(f"Formatted response: {formatted_response}")
        if formatted_response is not None:
            return formatted_response
        else:
            return {'error': 'No formatted response available'}

    def cache_history(self):
        return self.cache_manager.get_cache_history()
