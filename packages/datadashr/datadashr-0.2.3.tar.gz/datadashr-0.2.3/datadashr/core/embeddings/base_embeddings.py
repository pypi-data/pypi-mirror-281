class BaseEmbedding:
    def __init__(self, model_name=None, api_key=None):
        self.model_name = model_name or self.default_model_name
        self.api_key = api_key
        self.embedding_model = None

    @property
    def default_model_name(self):
        raise NotImplementedError("Subclasses should implement this property.")

    def check_requirements(self):
        raise NotImplementedError("Subclasses should implement this method.")

    def get_embedding(self):
        raise NotImplementedError("Subclasses should implement this method.")

    @property
    def model_info(self):
        return {
            "model_name": self.model_name,
            "api_key": self.api_key
        }
