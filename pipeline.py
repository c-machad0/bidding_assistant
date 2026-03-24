from langchain_community.vectorstores import Chroma
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import PromptTemplate
from langchain_openai import OpenAI, OpenAIEmbeddings


from prompts import TR_SECTION_PROMPT


class RagPipeline():

    def __init__(self):
        self.model = OpenAI(
            model='gpt-5-nano',
            temperature=0.2,
        )

        self.vector_store = Chroma(
            persist_directory='vector_db',
            embedding_function=OpenAIEmbeddings()
        )

        self.retriever = self.vector_store.as_retriever(
            search_kwargs={'k': 6}
        )

        self.prompt = PromptTemplate.from_template(TR_SECTION_PROMPT)

        self.chain = self.prompt | self.model | StrOutputParser()