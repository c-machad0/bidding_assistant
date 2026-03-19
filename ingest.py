import os
import re

from langchain_community.vectorstores import Chroma
from langchain_community.document_loaders import PyPDFLoader, Docx2txtLoader
from langchain_core.documents import Document
from langchain_openai import OpenAIEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter


from config import BASE_DIR

class RagIngest:

    def __init__(self):
        
        self.file_folder = 'data'

        self.docs = self.identify_doc()

        self.splitter = RecursiveCharacterTextSplitter(
            chunk_size = 500,
            chunk_overlap = 100,
        )

        self.embedding = OpenAIEmbeddings()
        self.persist_directory = 'vector_db'


    def get_logger(self, file_path):
        """
        Retorna o respectivo logger do arquivo na pasta.
        Ex: Se o arquivo for .pdf, ele vai renderizar o arquivo pelo PyPDFLoader
        """
        if file_path.endswith('.pdf'):
            return PyPDFLoader(file_path)
        elif file_path.endswith('.docx'):
            return Docx2txtLoader(file_path)


    def identify_doc(self):
        """
        Identifica qual tipo de documento será direcionado para fazer o RAG
        """

        data_path = os.path.join(BASE_DIR, self.file_folder)

        if not os.path.exists(data_path):
            raise FileNotFoundError("Pasta 'data' não encontrada")
        
        laws = os.path.join(BASE_DIR, "data", "laws")
        tr_models = os.path.join(BASE_DIR, "data", "tr_models")

        all_docs = []

        for folder in os.listdir(data_path):
            if folder == 'laws':
                docs = self.router_ingest(
                    folder_path=laws,
                    call_function=self.chunk_for_article
                )
                all_docs.extend(docs)

            elif folder == 'tr_models':
                docs = self.router_ingest(
                    folder_path=tr_models,
                    call_function=self.chunk_for_section
                )
                all_docs.extend(docs)

            else:
                raise FileNotFoundError("Pasta não encontrada")

        return all_docs 


    def router_ingest(self, folder_path, call_function):

        docs = []
        
        for file in os.listdir(folder_path):
            if file.endswith(('.pdf', '.doc', '.docx')):
                file_path = os.path.join(folder_path, file)
                loader = self.get_logger(file_path)

                pages = loader.load()

                full_text = "\n\n".join(page.page_content for page in pages)

                new_docs = call_function(full_text)

                docs.extend(new_docs)

        return docs
    

    def chunk_for_article(self, text: str) -> list[Document]:
        """
        Divide os chunks em artigos de Lei. Usada para quando a ingestão dos documentos for leis.
        """
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
                    }
            )
            documents.append(doc)

        return documents
    

    def chunk_for_section(self, text: str):

        pattern = r"(?ms)^(\d+)\.\s*(.+?)\n(.*?)(?=^\d+\.|\Z)"

        pattern_chunk = re.findall(pattern, text)

        documents = []

        for context in pattern_chunk:

            doc = Document(
                page_content=f"{context[0]}. {context[1]}\n{context[2]}",
                metadata={
                    "type_document": "termo de referêcia",
                    "section_title": context[1],
                }
            )

            documents.append(doc)

        return documents
    

    def doc_spliter(self):
        final_docs = []

        for doc in self.docs:
            if doc.metadata.get("type_document") == "lei":
                final_docs.append(doc)
            else:
                split = self.splitter.split_documents([doc])
                final_docs.extend(split)

        return final_docs
    

    def build_ingest(self):

        split_docs = self.doc_spliter()

        vector_store = Chroma.from_documents(
            documents=split_docs,
            persist_directory=self.persist_directory,
            embedding=self.embedding
        )

        vector_store.persist()
