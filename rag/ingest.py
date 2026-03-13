import os
import re

from langchain_community.vectorstores import Chroma
from langchain_community.document_loaders import PyPDFLoader
from langchain_core.documents import Document
from langchain_openai import OpenAIEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter


class RagIngest:

    def __init__(self):
        pdf_path = os.path.join("data", "L14133.pdf")
        loader = PyPDFLoader(pdf_path)
        self.docs = loader.load()

        self.splitter = RecursiveCharacterTextSplitter(
            chunk_size = 500,
            chunk_overlap = 100,
        )

        self.embedding = OpenAIEmbeddings()
        self.persist_directory = 'vector_db'


    def chunk_for_article(self, text: list) -> list[Document]:
        # Dividindo os chunks por artigos
        pattern = r'(Art\.?\s+\d+[º°o]?[\s\S]*?)(?=Art\.?\s+\d+[º°o]?|$)'
        articles = re.findall(pattern, text)

        documents = []

        # Para cada artigo, cria um Document
        for article in articles: # Transformando List[str] em List[Documents]
            doc = Document(
                page_content=article,
                metadata={
                    "type_document": "Lei 14133",
                    }
            )
            documents.append(doc)

        return documents
    

    def get_full_text(self) -> list[Document]:
        # Juntando todo conteúdo em um unico texto
        full_text = "\n".join(doc.page_content for doc in self.docs)
        articles = self.chunk_for_article(full_text)

        return articles
    

    def doc_splitter(self):
        documents = self.get_full_text()

        self.split_docs = self.splitter.split_documents(documents)

        return self.split_docs
    

    def build_ingest(self):

        split_docs = self.doc_splitter()

        vector_store = Chroma.from_documents(
            documents=split_docs,
            persist_directory=self.persist_directory,
            embedding=self.embedding
        )

        vector_store.persist()