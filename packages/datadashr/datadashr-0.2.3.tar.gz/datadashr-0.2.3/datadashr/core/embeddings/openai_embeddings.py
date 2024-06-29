from datadashr.core.embeddings.base_embeddings import BaseEmbedding
from datadashr.core.embeddings.check_embeddings import EmbeddingChecker


class OpenAIEmbedding(BaseEmbedding):
    @property
    def default_model_name(self):
        return "text-embedding-ada-002"

    def check_requirements(self):
        self.api_key = EmbeddingChecker.check_openai(self.model_name, self.api_key)

    def get_embedding(self):
        self.check_requirements()
        from langchain_openai import OpenAIEmbeddings
        return OpenAIEmbeddings(model=self.model_name, api_key=self.api_key)

    def embed_query(self, query):
        return self.get_embedding().embed_query(query)

    def embed_documents(self, document):
        return self.get_embedding().embed_documents(document)