import os
import pandas as pd
import polars as pl
import chromadb
import hashlib
from datadashr.config import VECTOR_DIR, logger
from langchain_chroma import Chroma
from datadashr.core.embeddings import Embedding
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import PyMuPDFLoader, TextLoader
from langchain_core.documents import Document
import trafilatura


class DatadashrDBVector:
    def __init__(self, db_path=VECTOR_DIR, collection_name='datadashr', embedding_type='ollama',
                 embedding_model='nomic-embed-text:latest', embedding_key=None, *args, **kwargs):
        self.db_path = db_path
        self.collection_name = collection_name
        self.reset_collection = kwargs.get('reset_collection', False)
        self.overwrite_file = kwargs.get('overwrite_file', False)
        self.client = chromadb.PersistentClient(path=self.db_path)
        if self.reset_collection:
            self._reset_collection()

        self.embeddings = Embedding(embedding_type=embedding_type, model_name=embedding_model, api_key=embedding_key)
        self.vectorstore = Chroma(embedding_function=self.embeddings, collection_name=self.collection_name,
                                  persist_directory=self.db_path, create_collection_if_not_exists=True)

        self.collection = self.client.get_collection(self.collection_name)

    def add_file(self, file_path):
        file_name = os.path.basename(file_path)
        if self.verify_if_file_exists(file_name):
            if self.overwrite_file:
                self.delete_file(file_name)
            else:
                logger.info(f"File {file_name} already exists in the collection")
                return

        file_type = self._get_file_type(file_path)
        documents = self._load_and_split(file_path, file_type)

        unique_documents = []
        for doc in documents:
            doc_hash = self._hash_document(doc)
            doc.metadata['document_hash'] = doc_hash
            if not self.verify_if_document_exists(doc):
                unique_documents.append(doc)
            else:
                logger.info(f"Duplicate document found and skipped: {doc.metadata}")

        if unique_documents:
            self.vectorstore.add_documents(unique_documents)

    def add_dataframe(self, df, source_name, dataframe_type='pandas', additional_metadata=None):
        if dataframe_type == 'polars' and isinstance(df, pd.DataFrame):
            raise ValueError("Provided dataframe is a Pandas DataFrame but 'polars' type was specified.")
        elif dataframe_type == 'pandas' and isinstance(df, pl.DataFrame):
            raise ValueError("Provided dataframe is a Polars DataFrame but 'pandas' type was specified.")

        if isinstance(df, pd.DataFrame):
            documents = self._process_pandas_dataframe(df, source_name, additional_metadata)
        elif isinstance(df, pl.DataFrame):
            documents = self._process_polars_dataframe(df, source_name, additional_metadata)
        else:
            raise ValueError("Unsupported dataframe type. Please provide a Pandas or Polars DataFrame.")

        unique_documents = []
        for doc in documents:
            doc_hash = self._hash_document(doc)
            doc.metadata['document_hash'] = doc_hash
            if not self.verify_if_document_exists(doc):
                unique_documents.append(doc)
            else:
                logger.info(f"Duplicate document found and skipped: {doc.metadata}")

        if unique_documents:
            self.vectorstore.add_documents(unique_documents)

    def _process_pandas_dataframe(self, df, source_name, additional_metadata):
        documents = []
        for _, row in df.iterrows():
            text = ' '.join([f"{col}: {val}" for col, val in row.items()])
            metadata = self._generate_metadata(row, source_name, 'pandas', additional_metadata)
            documents.append(Document(page_content=text, metadata=metadata))
        return documents

    def _process_polars_dataframe(self, df, source_name, additional_metadata):
        documents = []
        for row in df.iter_rows(named=True):
            text = ' '.join([f"{col}: {val}" for col, val in row.items()])
            metadata = self._generate_metadata(row, source_name, 'polars', additional_metadata)
            documents.append(Document(page_content=text, metadata=metadata))
        return documents

    def _generate_metadata(self, row, source_name, dataframe_type, additional_metadata, document_hash=None):
        metadata = {'source_name': source_name, 'dataframe_type': dataframe_type, 'document_hash': document_hash}
        if additional_metadata:
            metadata.update(additional_metadata)

        filtered_metadata = {k: v for k, v in metadata.items() if self._is_supported_metadata(v)}

        row_metadata = {f'col_{k}': v for k, v in row.items() if self._is_supported_metadata(v)}
        filtered_metadata.update(row_metadata)

        return filtered_metadata

    @staticmethod
    def _is_supported_metadata(value):
        return isinstance(value, (str, int, float, bool)) and (not isinstance(value, str) or len(value) < 100)

    def _get_file_type(self, file_path):
        _, ext = os.path.splitext(file_path)
        return ext.lower()

    def _load_and_split(self, file_path, file_type):
        if file_type == '.pdf':
            return self._process_pdf(file_path)
        elif file_type == '.txt':
            return self._process_txt(file_path)
        elif file_type == '.html':
            return self._process_html(file_path)
        elif file_type == '.csv':
            return self._process_csv(file_path)
        elif file_type == '.xlsx' or file_type == '.xls':
            return self._process_excel(file_path)
        elif file_type == '.parquet':
            return self._process_parquet(file_path)
        else:
            raise ValueError(f"Unsupported file type: {file_type}")

    def _process_pdf(self, file_path):
        loader = PyMuPDFLoader(file_path)
        text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=0)
        return self._load_and_split_documents(loader, text_splitter, file_path, 'pdf')

    def _process_txt(self, file_path):
        loader = TextLoader(file_path)
        text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
        return self._load_and_split_documents(loader, text_splitter, file_path, 'txt')

    def _process_html(self, file_path):
        with open(file_path, 'r', encoding='utf-8') as file:
            content = file.read()

        result = trafilatura.extract(content, include_formatting=True, include_comments=False, no_fallback=True)
        if result is None:
            raise ValueError(f"Failed to extract content from {file_path}")

        metadata = trafilatura.extract_metadata(content)
        text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=0)
        splits = text_splitter.split_text(result)

        return [
            Document(page_content=split,
                     metadata={'file_name': os.path.basename(file_path), 'file_type': 'html', **metadata})
            for idx, split in enumerate(splits)
        ]

    def _process_csv(self, file_path):
        data = pd.read_csv(file_path)
        return self._process_pandas_dataframe(data, os.path.basename(file_path))

    def _process_excel(self, file_path):
        data = pd.read_excel(file_path)
        return self._process_pandas_dataframe(data, os.path.basename(file_path))

    def _process_parquet(self, file_path):
        data = pd.read_parquet(file_path)
        return self._process_pandas_dataframe(data, os.path.basename(file_path))

    def _load_and_split_documents(self, loader, text_splitter, file_path, file_type):
        documents = loader.load()
        new_documents = []

        logger.info(f"Loaded {len(documents)} documents from {file_path}")

        for doc in documents:
            new_metadata = doc.metadata.copy()
            new_metadata.update({'file_name': os.path.basename(file_path), 'file_type': file_type})
            new_doc = Document(page_content=doc.page_content, metadata=new_metadata)
            new_documents.append(new_doc)

        return text_splitter.split_documents(new_documents)

    def query(self, query_text):
        embedding = self.embeddings.embed_query(query_text)
        return self.collection.query(embedding, n_results=3)

    def delete_file(self, file_name):
        results = self.collection.query(
            query_embeddings=self.embeddings.embed_query("dummy query"),  # Necessario per attivare la query
            n_results=1000,  # Numero elevato per assicurarsi di trovare tutti i documenti
            where={"file_name": file_name}
        )
        ids_to_delete = [result['id'] for result in results['documents']]
        self.collection.delete(ids=ids_to_delete)

    def verify_if_file_exists(self, file_name) -> bool:
        results = self.collection.query(
            query_embeddings=self.embeddings.embed_query("dummy query"),  # Necessario per attivare la query
            n_results=1,  # Numero elevato per assicurarsi di trovare tutti i documenti
            where={"file_name": file_name},
            include=["metadatas"]
        )
        logger.info(f"Found {len(results['metadatas'][0])} documents with file name {file_name}")
        return len(results['metadatas'][0]) > 0

    def get_collection(self, limit=10, offset=0):
        return self.collection.get(include=["metadatas"], limit=limit, offset=offset)

    def _reset_collection(self):
        logger.info(f"Checking if collection {self.collection_name} exists")
        existing_collections = self.client.list_collections()
        if self.collection_name in [col.name for col in existing_collections]:
            self.client.delete_collection(self.collection_name)
            logger.info(f"Deleted collection {self.collection_name}")

    def _hash_document(self, document):
        hasher = hashlib.md5()
        hasher.update(document.page_content.encode('utf-8'))
        for key, value in document.metadata.items():
            hasher.update(f"{key}:{value}".encode('utf-8'))
        return hasher.hexdigest()

    def verify_if_document_exists(self, document):
        document_hash = self._hash_document(document)
        results = self.collection.query(
            query_embeddings=self.embeddings.embed_query("dummy query"),  # Necessario per attivare la query
            n_results=1,  # Numero di risultati per assicurarsi di trovare il documento
            where={"document_hash": document_hash},
            include=["metadatas"]
        )
        # Controllo se 'documents' è None o vuoto
        if results is None or 'documents' not in results or not results['documents']:
            return False
        return len(results['documents']) > 0

