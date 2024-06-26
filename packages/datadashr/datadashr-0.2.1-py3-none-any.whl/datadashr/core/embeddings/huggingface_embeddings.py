from datadashr.core.embeddings.base_embeddings import BaseEmbedding
from datadashr.core.embeddings.check_embeddings import EmbeddingChecker


class HuggingfaceEmbedding(BaseEmbedding):
    @property
    def default_model_name(self):
        return "mixedbread-ai/mxbai-embed-large-v1"

    def check_requirements(self):
        pass

    def get_embedding(self):
        self.check_requirements()
        from langchain_huggingface.embeddings import HuggingFaceEmbeddings
        return HuggingFaceEmbeddings(model_name=self.model_name)

    def embed_query(self, query):
        return self.get_embedding().embed_query(query)

    def embed_documents(self, document):
        return self.get_embedding().embed_documents(document)
