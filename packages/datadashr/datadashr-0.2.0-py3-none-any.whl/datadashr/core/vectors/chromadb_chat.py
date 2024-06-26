from datadashr.config import VECTOR_DIR, logger
from datadashr.core.llm import OllamaLLM
from datadashr.core.importers.vector.chromadb_vector import ChromaDBVector


class ChromaDBChat:
    def __init__(self, llm_instance, vector_instance):
        self.db = vector_instance
        self.llm = llm_instance

    def prompt(self, query):
        results = self.db.query(query)
        logger.info(f"Query Results: {results}")

        # Limitiamo il numero di documenti e la lunghezza del contesto
        max_context_length = 2000  # Limite di caratteri per il contesto
        context = ""
        for sublist in results['documents']:
            for doc in sublist:
                if len(context) + len(doc) > max_context_length:
                    break
                context += doc + "\n"
            if len(context) > max_context_length:
                break
        return [
            {"role": "user",
             "content": f"You are an assistant for question-answering tasks. Use the following pieces of retrieved context to answer the question. If you don't know the answer, just say that you don't know. Use three sentences maximum and keep the answer concise.Context:\n{context}\n\nQuestion: {query}\nAnswer:"},
        ]

    def chat(self, query):
        response = self.llm.chat(self.prompt(query))
        logger.info(f"Query Response: {response}")
        return response


if __name__ == '__main__':
    llm = OllamaLLM(model='llama3', params={"temperature": 0.0}, verbose=True)
    vector = ChromaDBVector(db_path=VECTOR_DIR, collection_name='datadashr', embedding_type='ollama',
                            embedding_model='nomic-embed-text:latest', embedding_key=None)
    chat = ChromaDBChat(llm_instance=llm, vector_instance=vector)
    result = chat.chat('Cosa dice il presidente Zelenskyy?')
    logger.info(result)
