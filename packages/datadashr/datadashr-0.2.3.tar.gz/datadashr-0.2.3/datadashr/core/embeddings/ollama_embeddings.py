from datadashr.core.embeddings.base_embeddings import BaseEmbedding
from datadashr.core.embeddings.check_embeddings import EmbeddingChecker
from datadashr.config import *


class OllamaEmbedding(BaseEmbedding):
    @property
    def default_model_name(self):
        return "nomic-embed-text:latest"

    def check_requirements(self):
        EmbeddingChecker.check_ollama(self.model_name)

    def get_embedding(self):
        self.check_requirements()
        from langchain_community.embeddings import OllamaEmbeddings
        return OllamaEmbeddings(model=self.model_name)

    def embed_query(self, query):
        return self.get_embedding().embed_query(query)

    def embed_documents(self, document):
        return self.get_embedding().embed_documents(document)

