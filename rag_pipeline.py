import os
import re

from langchain_community.vectorstores import Chroma
from langchain_community.document_loaders import PyPDFLoader
from langchain_core.documents import Document
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter



class RagPipeline:
    def __init__(self):
        self.model = ChatOpenAI(
            model='gpt-4o-mini',
            temperature=0.2,
        )

        self.pdf_path = os.path.join("data", "L14133.pdf")
        self.loader = PyPDFLoader(self.pdf_path)
        self.docs = self.loader.load()

        self.embedding = OpenAIEmbeddings()
        self.persist_directory = 'vector_db'


    def chunk_for_article(self, text: list) -> list[Document]:
        # Dividindo os chunks por artigos
        pattern = r'(Art\.?\s+\d+[º°o]?[\s\S]*?)(?=Art\.?\s+\d+[º°o]?|$)'
        articles = re.findall(pattern, text)

        self.documents = []

        for article in articles: # Transformando List[str] em List[Documents]
            doc = Document(
                page_content=article,
                metadata={"fonte": "Lei 14133"}
            )
            self.documents.append(doc)

        return self.documents
    
    
    def get_full_text(self) -> list[Document]:
        # Juntando todo conteúdo em um unico texto
        self.full_text = "\n".join(doc.page_content for doc in self.docs)
        self.articles = self.chunk_for_article(self.full_text)

        return self.articles
    

    def text_splitter(self):
        self.splitter = RecursiveCharacterTextSplitter(
            chunk_size = 1200,
            chunk_overlap = 200,
        )

        return self.splitter
    
    
    def set_vector_store(self):

        splitter = self.text_splitter()

        documents = self.get_full_text()

        split_docs = splitter.split_documents(documents)

        try:
            self.vector_store = Chroma(
                persist_directory=self.persist_directory,
                embedding_function=self.embedding
            )
        except:
            self.vector_store = Chroma.from_documents(
                documents=split_docs,
                persist_directory=self.persist_directory,
                embedding=self.embedding
            )

        return self.vector_store
    

    def retriever_vector_store(self):
        self.retriever = self.vector_store.as_retriever()

        return self.retriever
    
    
    def set_user_prompt(self, chat_system_prompt):
        self.prompt = ChatPromptTemplate.from_messages([
            ("system", chat_system_prompt),
            ("human", """
            Use apenas o contexto abaixo para responder.

            Contexto:
            {context}

            Pergunta:
            {question}
            """)
        ])

        return self.prompt
    
    
    def set_rag_chain(self):
        self.rag_chain = (
            {
                "context": self.retriever,
                "question": RunnablePassthrough()
            }
            |self.prompt
            |self.model
            |StrOutputParser()
        )

        return self.rag_chain