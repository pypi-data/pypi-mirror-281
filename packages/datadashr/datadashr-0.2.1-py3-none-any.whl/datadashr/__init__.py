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
    FormatResponseStep, SaveCacheStep, ExtractQueriesStep, ExecuteQueriesStep, ValidateQueriesStep
from datadashr.core.importers import Connector
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
        self.prompt_manager = PromptManager(data_connector=self.data_connector,
                                            custom_prompt=kwargs.get('custom_prompt', ""),
                                            prompt_override=kwargs.get('prompt_override', False),
                                            data_connector_type=self.data_connector_type,
                                            verbose=self.verbose)
        self.ut = Utilities(self.verbose)
        self.enable_cache = kwargs.get('enable_cache', False)
        self.format_type = kwargs.get('format_type', 'api')

        self.data_connector.import_data(data, reset=self.reset_db)

        self.request = None

    def chat(self, request):
        if self.verbose:
            logger.info(f"Executing pipeline for request: {request}")
        self.request = request
        requests = [
            "Thanks for this request {request}, I was just thinking I wanted to do this!",
            "Wow, {request}? That's an interesting one! Let's dive in!",
            "Hey there! You've got a question about {request}, and I've got answers!",
            "Oh, {request}? Perfect timing, I was just waiting for this one!",
            "Your question about {request} has just made my day! Let's solve it!",
            "Great choice asking about {request}! Let's get to work!",
            "Awesome, {request}? Let's make this fun!",
            "You know, I was just thinking about {request} too! Let's tackle it together!",
            "Oh, {request}? This is going to be exciting!",
            "I'm thrilled you asked about {request}! Let's jump right in!",
            "Guess what? {request} is my specialty! Let's get started!",
            "I'm so glad you asked about {request}! Let's figure it out!",
            "Your question about {request} just made my day better!",
            "Fantastic! A {request} question. Let’s get cracking!",
            "Oh, {request}? I've got just the thing for you!",
            "I’ve been waiting for someone to ask about {request}! Let’s do this!",
            "You’re curious about {request}? So am I! Let’s explore together!",
            "Sweet! A {request} query. Let’s dive right in!",
            "A {request} question, you say? Let's tackle it together!",
            "Oh, cool! You’re asking about {request}? Let’s get to it!",
            "I see you have a question about {request}. Let's solve it with style!",
            "A {request} question? This is going to be fun!",
            "Alright! You want to know about {request}? Let's make it happen!",
            "Perfect timing! I was just in the mood for a {request} question!",
            "Ah, a {request} query! Let’s get started!",
            "I love questions about {request}! Let’s jump in!",
            "Fantastic, {request}? Let’s see what we can do!",
            "Your {request} question is music to my ears! Let’s get on it!",
            "I’m excited about {request} too! Let’s get this answered!",
            "Great, a {request} question! Let’s find the answer together!"
        ]
        logger.info(random.choice(requests).format(request=request))

        context = {
            'llm_instance': self.llm_instance,
            'data_connector': self.data_connector,
            'cache_manager': self.cache_manager,
            'prompt_manager': self.prompt_manager,
            'utilities': self.ut,
            'request': request,
            'enable_cache': self.enable_cache,
            'format_type': self.format_type,
            'chart_dir': self.chart_dir,
            'data_connector_type': self.data_connector_type,
            'verbose': self.verbose,
        }

        step = Pipeline(**context)
        step.add_step(CacheStep("Cache"))
        step.add_step(PromptGenerationStep("PromptGeneration"))
        step.add_step(LLMRequestStep("LLMRequest"))
        step.add_step(ExtractQueriesStep("ExtractQueries"))
        step.add_step(ValidateQueriesStep("ValidateQueries"))
        step.add_step(ErrorHandlingStep("ErrorHandling"))
        step.add_step(ExecuteQueriesStep("ExecuteQueries"))
        step.add_step(FormatResponseStep("FormatResponse"))
        step.add_step(SaveCacheStep("SaveCache"))

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
