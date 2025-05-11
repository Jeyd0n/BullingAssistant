from typing import Optional, List
from langchain.tools import BaseTool
from langchain.schema import Document
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.vectorstores import Chroma
import chromadb


class ChromaVectorTool(BaseTool):
    name: str = 'vector_search'
    description: str = '''Инструмент поиска по векторной базе знаний с использованием Chroma.
                    Полезен, когда пользователь спрашивает о локальных данных, документации или контенте, 
                    доступном внутри базы знаний'''

    def __init__(
        self,
        collection_name: str = 'docs',
        host: str = 'localhost',
        port: int = 8000,
        embedding_model_name: str = 'sentence-transformers/all-MiniLM-L6-v2',
        chunk_size: int = 500,
        chunk_overlap: int = 50,
    ):
        '''
        Инициализация векторной базы Chroma с нужным эмбеддером.


        '''
        super().__init__()
        self.splitter = RecursiveCharacterTextSplitter(chunk_size=chunk_size,
                        chunk_overlap=chunk_overlap, separators=["\n\n", "\n", ".", " ", ""])
        self.embeddings = HuggingFaceEmbeddings(model_name=embedding_model_name)
        self.client = chromadb.HttpClient(host=host, port=port)
        if collection_name not in [collection.name for collection in self.client.list_collections()]:
            self.client.create_collection(name=collection_name)

        self.vectorstore = Chroma(client=self.client, collection_name=collection_name,
                            embedding_function=self.embeddings)
        

    def _run(self, query: str) -> str:
        '''
        Поиск релевантных документов по текстовому запросу.

        Args:
            query (str): Вопрос пользователя или ключевая фраза.

        Returns:
            str: Контекст, составленный из найденных документов.


        '''
        docs: List[Document] = self.vectorstore.similarity_search(query, k=3)
        if not docs:
            return 'Контекст не найден в базе знаний.'
        
        return '\n\n'.join([doc.page_content for doc in docs])

    def add_documents(self, texts: List[str]) -> None:
        '''
        Добавляет текст в базу, автоматически разбивая на чанки.

        Args:
            texts (List[str]): Список строк, каждая из которых — отдельный документ.


        '''
        all_chunks = []
        for raw_text in texts:
            chunks = self.splitter.create_documents([raw_text])
            all_chunks.extend(chunks)
        self.vectorstore.add_documents(all_chunks)

    def clear(self) -> None:
        '''
        Полностью очищает коллекцию документов в Chroma.


        '''
        self.vectorstore.delete_collection()
