import os
import re

from langchain_community.vectorstores import Chroma
from langchain_community.document_loaders import PyPDFLoader
from langchain_core.documents import Document
from langchain_openai import OpenAIEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter


class RagIngest:

    def __init__(self):
        self.pdf_folder = 'data'

        self.docs = self.load_file_for_rag()

        self.splitter = RecursiveCharacterTextSplitter(
            chunk_size = 500,
            chunk_overlap = 100,
        )

        self.embedding = OpenAIEmbeddings()
        self.persist_directory = 'vector_db'


    def load_file_for_rag(self):

        docs = []

        if not os.path.exists(self.pdf_folder):
            raise FileNotFoundError("Pasta 'data' não encontrada.")

        for pdf_file in os.listdir(self.pdf_folder):
            if pdf_file.endswith(".pdf"):
                pdf_path = os.path.join(self.pdf_folder, pdf_file)
                loader = PyPDFLoader(pdf_path)

                pages = loader.load()

                # Juntando todo conteúdo em um unico texto
                full_text = "\n\n".join(page.page_content for page in pages)
                article_docs = self.chunk_for_article(full_text, pdf_file)

                docs.extend(article_docs)

        return docs
    

    def chunk_for_article(self, text: str, source: str) -> list[Document]:
        # Dividindo os chunks por artigos
        pattern = r'(Art\.?\s+\d+[º°o]?[\s\S]*?)(?=Art\.?\s+\d+[º°o]?|$)'
        articles = re.findall(pattern, text)

        documents = []

        # Para cada artigo, cria um Document
        for article in articles: # Transformando List[str] em List[Documents]
            doc = Document(
                page_content=article,
                metadata={
                    "type_document": "lei",
                    "source": source
                    }
            )
            documents.append(doc)

        return documents
    

    def doc_splitter(self):
        documents = self.docs

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