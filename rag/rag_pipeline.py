from langchain_community.vectorstores import Chroma
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough
from langchain_openai import ChatOpenAI, OpenAIEmbeddings



from prompts import CHAT_SYSTEM_PROMPT


class RagPipeline():

    def __init__(self):
        self.model = ChatOpenAI(
            model='gpt-4o-mini',
            temperature=0.2,
        )

        self.vector_store = Chroma( # Carregando dados do vector_store
            persist_directory='vector_db',
            embedding_function=OpenAIEmbeddings()
        )

        self.retriever = self.vector_store.as_retriever(
            search_kwargs={"k": 3},
            filter={"source": "14133"}
        )

        self.chat_prompt = ChatPromptTemplate.from_messages([
            ("system", CHAT_SYSTEM_PROMPT),
            ("human", """
            Use apenas o contexto abaixo para responder.

            Contexto:
            {context}

            Pergunta:
            {question}
            """)
        ])

        self.chat_chain = (
            {
                "context": self.retriever | self.format_docs, # docs = self.retriever.invoke("dispensa de licitação")
                "question": RunnablePassthrough()
            }
            |self.chat_prompt
            |self.model
            |StrOutputParser()
        )

    
    def format_docs(self, docs):
        # Transforma os documentos recuperados em um texto unico
        return "\n\n".join(doc.page_content for doc in docs)