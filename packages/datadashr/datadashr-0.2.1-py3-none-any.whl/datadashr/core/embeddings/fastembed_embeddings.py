from datadashr.core.embeddings.base_embeddings import BaseEmbedding
from datadashr.core.embeddings.check_embeddings import EmbeddingChecker


class FastembedEmbedding(BaseEmbedding):
    @property
    def default_model_name(self):
        return "BAAI/bge-small-en-v1.5"

    def check_requirements(self):
        pass

    def get_embedding(self):
        self.check_requirements()
        from langchain_community.embeddings.fastembed import FastEmbedEmbeddings
        return FastEmbedEmbeddings()

    def embed_query(self, query):
        return self.get_embedding().embed_query(query)

    def embed_documents(self, document):
        return self.get_embedding().embed_documents(document)
