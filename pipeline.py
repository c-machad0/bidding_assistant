from queries import SECTION_QUERIES

from langchain_core.prompts import PromptTemplate
from langchain_openai import ChatOpenAI


class RagPipeline:

    def __init__(self, vectorstore):
        self.vectorstore = vectorstore

        self.retriever = vectorstore.as_retriever(search_kwargs={"k": 4})
        self.chain = self._build_chain()


    def generate_section(self, section, data, previous_sections=""):

        query = self._build_query(section, data)
        docs = self.retriever.invoke(query)
        context = self._format_context(docs)

        # 🎯 regra específica por seção
        format_rules = ""

        if section in ["ob_contratante", "ob_contratada"]:
            format_rules = "- Estruture a resposta em lista com marcadores (bullet points)"

        response = self.chain.invoke({
            "context": context,
            "section_name": section,
            "previous_sections": previous_sections,
            "format_rules": format_rules,
            **data
        })

        return response.content.strip()


    def _build_query(self, section, data):
        base_query = SECTION_QUERIES.get(section, "")

        return f"""
        {base_query}
        objeto da contratação: {data.get('objeto_tr', '')}
        modalidade: {data.get('bidding_modality', '')}
        """


    def _format_context(self, docs):
        return "\n\n".join(
            doc.page_content[:500] for doc in docs
        )


    def _build_chain(self):

        prompt = PromptTemplate(
            input_variables=[
                "context",
                "section_name",
                "previous_sections",
                "objeto_tr",
                "select_secretary",
                "start_date",
                "end_date",
                "bidding_modality",
                "base_value"
            ],
            template="""
    Você é um especialista em licitações públicas.

    Elabore a seção "{section_name}" de um Termo de Referência.

    Regras:
    - Linguagem formal
    - Baseado no contexto
    - Não inventar informações
    - Evitar repetições
    - NÃO escreva o nome da seção no início da resposta

    {format_rules}

    Seções anteriores:
    {previous_sections}

    Contexto:
    {context}

    Dados:
    Objeto: {objeto_tr}
    Secretaria: {select_secretary}
    Período: {start_date} até {end_date}
    Modalidade: {bidding_modality}
    Valor estimado: {base_value}
    """
        )

        llm = ChatOpenAI(temperature=0)

        return prompt | llm