import subprocess
import ollama
import webbrowser
import polars as pl
import uuid
import logging
from datadashr import DataDashr
from datadashr.core.llm import OllamaLLM
from datadashr.core.importers import Connector
from datadashr.config import *
from pywebio import start_server
from pywebio.input import file_upload, select, checkbox, input
from pywebio.output import put_text, popup

# Setup logger
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
ch = logging.StreamHandler()
ch.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
ch.setFormatter(formatter)
logger.addHandler(ch)


class App:
    def __init__(self):
        self.allowed_models = ['codestral', 'mixtral']
        self.available_models = []

        self.llm_selector = None
        self.cache_switch = True
        self.verbose_switch = False
        self.file_input = None
        self.df = None

    def initialize_app(self):
        if not self.verify_if_ollama_server_is_running() or not self.check_ollama_list():
            logger.error("Ollama server is not available. Please check the installation.")
            return

        self.available_models = self.check_accepted_models()
        if not self.available_models:
            logger.error("None of the accepted models are available.")
            return

        self.llm_selector = self.available_models[0] if self.available_models else None

    def get_allama_llm_list(self):
        models = ollama.list()
        return [model['name'] for model in models['models']]

    def verify_if_ollama_server_is_running(self):
        try:
            models = ollama.list()
            return True
        except Exception as e:
            logger.error(f"Ollama server is not running: {e}")
            return False

    def check_ollama_list(self):
        try:
            result = subprocess.run(['ollama', 'list'], capture_output=True, text=True, check=True)
            if result.stdout:
                return True
            logger.error("Ollama server is not running")
            webbrowser.open('https://ollama.com/download')
            return False
        except subprocess.CalledProcessError as e:
            logger.error(f"Error checking ollama list: {e}")
            return False

    def check_accepted_models(self):
        models = self.get_allama_llm_list()
        if not models:
            logger.error("Nessun modello disponibile.")
            return []

        available_models = []
        logger.info(f"Models: {models}")

        normalized_models = {model.split(':')[0]: model for model in models}

        for model in self.allowed_models:
            logger.info(f"Checking model: {model}")
            if model in normalized_models:
                logger.info(f"Modello accettato: {model}")
                available_models.append(normalized_models[model])

        if not available_models:
            logger.error("Nessuno dei modelli accettati è disponibile.")
            return []

        return available_models

    def update_datadashr(self):
        selected_llm = self.llm_selector
        enable_cache = self.cache_switch
        enable_verbose = self.verbose_switch

        if not self.file_input:
            logger.error("File CSV non caricato. Carica un file per continuare.")
            put_text("Please upload a CSV file to proceed.")
            return

        # generate random file name to avoid conflicts
        file_name = f"{uuid.uuid4()}.csv"
        file_path = os.path.join(CSV_DIR, file_name)

        # create the file and write the content of the file input
        with open(file_path, 'wb') as f:
            f.write(self.file_input['content'])

        connector = Connector(filepaths=file_path)
        self.df = DataDashr(
            data_connector=connector,
            llm_instance=OllamaLLM(model=selected_llm, params={"temperature": 0.0}, verbose=enable_verbose),
            verbose=enable_verbose,
            enable_cache=enable_cache,
            format_type='panel'
        )

        try:
            self.df.df = pl.read_csv(file_path)
        except Exception as e:
            logger.error(f"Error {e} decoding the CSV file. Try loading a file with a different encoding.")
            put_text("Error decoding the CSV file. Please upload a file with a different encoding.")
            return

    def generate_response(self, contents: str):
        if not self.df:
            put_text("Please upload a CSV file to start the analysis.")
            return

        logger.info(f"Request: {contents}")
        response = self.df.chat(contents)
        put_text(response)

    def serve(self):
        self.initialize_app()

        if not self.available_models:
            put_text("No accepted models available. Please check your configuration.")
            return

        file_info = file_upload("Upload CSV", accept=".csv")
        self.file_input = file_info

        model = select("Select LLM", options=self.available_models)
        self.llm_selector = model

        settings = checkbox("Settings", options=["Enable Cache", "Enable Verbose"])

        self.cache_switch = "Enable Cache" in settings
        self.verbose_switch = "Enable Verbose" in settings

        self.update_datadashr()

        popup('Datadashr Chat', 'Hi! How can I help you?')

        while True:
            contents = input("You:", type='text')
            if contents.lower() == 'exit':
                break
            self.generate_response(contents)


if __name__ == '__main__':
    start_server(App().serve, port=8080, debug=True)
