from datadashr.core.embeddings.openai_embeddings import OpenAIEmbedding
from datadashr.core.embeddings.ollama_embeddings import OllamaEmbedding
from datadashr.core.embeddings.fastembed_embeddings import FastembedEmbedding
from datadashr.core.embeddings.huggingface_embeddings import HuggingfaceEmbedding


class Embedding:
    EMBEDDING_CLASSES = {
        'openai': OpenAIEmbedding,
        'ollama': OllamaEmbedding,
        'fastembed': FastembedEmbedding,
        'huggingface': HuggingfaceEmbedding
    }

    def __new__(cls, embedding_type, model_name=None, api_key=None):
        if embedding_type not in cls.EMBEDDING_CLASSES:
            raise ValueError(f"Unsupported embedding type: {embedding_type}")
        embedding_class = cls.EMBEDDING_CLASSES[embedding_type]
        embedding_instance = embedding_class(model_name, api_key)
        embedding_instance.get_embedding()  # Initialize the embedding model
        return embedding_instance

    @classmethod
    def available_embeddings(cls):
        return list(cls.EMBEDDING_CLASSES.keys())


# Esempio di utilizzo
if __name__ == "__main__":
    available_embeddings = Embedding.available_embeddings()
    print(f"Available embeddings: {available_embeddings}")

    # Utilizzo con modello specificato e chiave API
    """factory = EmbeddingFactory(embedding_type='ollama', model_name='snowflake-arctic-embed', api_key=None)
    embedding = factory.get_embedding()
    print(embedding)"""

    # Utilizzo con modello di default senza chiave API
    embedding = Embedding(embedding_type='fastembed')
    print(embedding.model_info)
    print(embedding.embed_query('Hello, world!'))

    embedding = Embedding(embedding_type='ollama')
    print(embedding.model_info)
    print(embedding.embed_query('Hello, world!'))

    embedding = Embedding(embedding_type='huggingface')
    print(embedding.model_info)
    print(embedding.embed_query('Hello, world!'))
