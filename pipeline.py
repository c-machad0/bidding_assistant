from langchain_community.vectorstores import Chroma
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI, OpenAIEmbeddings

from prompts import TR_SECTION_PROMPT


class RagPipeline():

    def __init__(self, vectorstore):
        self.model = ChatOpenAI(
            model='gpt-4o-mini',
            temperature=0.2,
        )

        self.vector_store = vectorstore

        self.retriever = self.vector_store.as_retriever(
            search_kwargs={'k': 4}
        )

        self.prompt = ChatPromptTemplate.from_template(TR_SECTION_PROMPT)

        self.chain = self.prompt | self.model | StrOutputParser()