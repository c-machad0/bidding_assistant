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


class Service:
    def __init__(self):
        self.model = ChatOpenAI(
            model='gpt-4o-mini',
            temperature=0
        )

        self.pdf_path = 'L14133.pdf'
        self.loader = PyPDFLoader(self.pdf_path)
        self.docs = self.loader.load()

        self.embedding = OpenAIEmbeddings()
        self.persist_directory = 'licita_database'

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

        if os.path.exists(self.persist_directory):
            self.vector_store = Chroma(
                persist_directory=self.persist_directory,
                embedding_function=self.embedding
            )
        else:
            self.vector_store = Chroma.from_documents(
                documents=split_docs,
                persist_directory=self.persist_directory,
                embedding_function=self.embedding
            )

        return self.vector_store
    

    def retriever_vector_store(self):
        self.retriever = self.vector_store.as_retriever()

        return self.retriever

    def get_system_prompt(self):
        self.system_prompt = """
        Você é um assistente jurídico especializado em legislação de licitações públicas brasileiras,
        especialmente na Lei 8.666/1993 e na Lei 14.133/2021.

        Seu papel é responder perguntas utilizando EXCLUSIVAMENTE as informações recuperadas
        do banco de dados de leis fornecido pelas ferramentas disponíveis.

        Diretrizes obrigatórias:

        1. Baseie suas respostas apenas no conteúdo encontrado nos documentos.
        2. Sempre que possível, mencione o número do artigo, parágrafo ou inciso que fundamenta sua resposta.
        3. Não invente informações nem complemente com conhecimento externo.
        4. Caso a informação não esteja disponível na base consultada, informe claramente que
        não foi possível localizar fundamento legal suficiente.
        5. Explique de forma clara, técnica e objetiva, mas com linguagem acessível.
        6. Estruture a resposta de forma organizada quando necessário (ex: tópicos, etapas, requisitos).
        7. Sempre responda em português brasileiro.
        8. A resposta final deve ser amigável, clara e útil ao usuário.

        Responda em formato markdown bem estruturado.
        """

        return self.system_prompt
    
    def set_user_prompt(self):
        self.prompt = ChatPromptTemplate.from_messages([
            ("system", self.system_prompt),
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
    
    def ask_question(self, question: str):
        return self.rag_chain.invoke(question)

    def build_service(self):
        self.set_vector_store()
        self.retriever_vector_store()
        self.get_system_prompt()
        self.set_user_prompt()
        self.set_rag_chain()


if __name__ == "__main__":
    service = Service()
    response = service.build_service()

    user_question = 'Quero fazer uma dispensa para contratação de serviços de dedetização para as escolas do município. Qual inciso eu uso?'

    response = service.set_rag_chain().invoke(user_question)

    print(response)