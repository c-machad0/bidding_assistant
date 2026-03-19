import os


import streamlit as st


from config import BASE_DIR, sections
from docxtpl import DocxTemplate
from interface import date_execution, objeto_tr, select_secretary, bidding_modality, base_value
from ingest import RagIngest
from pipeline import RagPipeline


class App():

    def __init__(self):
        self.rag = RagPipeline()

        if not os.path.exists("vector_db"): # verifica se o vector_db existe
            ingest = RagIngest()
            ingest.build_ingest()

    
    def generate_tr(self, query):

        result = {}

        template_path = os.path.join(
            BASE_DIR,
            "documents",
            "modelo_tr_dispensa.docx"
        )

        doc = DocxTemplate(template_path)

        # tratar datas
        if isinstance(date_execution, tuple):
            data_inicio, data_fim = date_execution
            date_execution_str = f"{data_inicio} a {data_fim}"
        else:
            date_execution_str = str(date_execution)

        for section in sections:

            # query para RAG por seção
            query = f"Termo de referência seção {section}"

            docs = self.rag.retriever.invoke(query)

            context = "\n\n".join([doc.page_content for doc in docs])

            response = self.rag.chain.invoke({
                "context": context,
                "objeto_tr": objeto_tr,
                "select_secretary": select_secretary,
                "date_execution": date_execution_str,
                "bidding_modality": bidding_modality,
                "base_value": base_value,
                "section_name": section
            })

            result[section] = response

        outputh_path = os.path.join(BASE_DIR, 'documents', 'novo_tr.docx')

        doc.render(result)
        doc.save(outputh_path)

        with open(outputh_path, "rb") as file:
            file_bytes = file.read()

        st.download_button(
            label="Download Termo de Referência",
            data=file_bytes,
            file_name="novo_tr.docx",
        )

        st.success("Termo de Referência gerado com sucesso!")