import os
from io import BytesIO
from datetime import date


from config import BASE_DIR, sections
from docxtpl import DocxTemplate
from ingest import RagIngest
from pipeline import RagPipeline


class App():

    def __init__(self, vectorstore):
        self.rag = RagPipeline(vectorstore)

    
    def generate_tr(self, data):

        result = {}

        objeto_tr = data["objeto_tr"]
        select_secretary = data["select_secretary"]
        start_date = data["start_date"]
        end_date = data["end_date"]
        bidding_modality = data["bidding_modality"]
        base_value = data["base_value"]

        template_path = os.path.join(
            BASE_DIR,
            "templates",
            "modelo_tr.docx"
        )

        doc = DocxTemplate(template_path)

        # tratar datas
        start_date_str = start_date.strftime("%d/%m/%Y")
        end_date_str = end_date.strftime("%d/%m/%Y")

        for section in sections:

            # query para RAG por seção
            query = f"Termo de referência seção {section}"

            docs = self.rag.retriever.invoke(query)

            context = "\n\n".join([doc.page_content for doc in docs])

            response = self.rag.chain.invoke({
                "context": context,
                "objeto_tr": objeto_tr,
                "select_secretary": select_secretary,
                "start_date": start_date_str,
                "end_date": end_date_str,
                "bidding_modality": bidding_modality,
                "base_value": base_value,
                "section_name": section
            })

            result[section] = response

        doc.render(result)

        file_stream = BytesIO()
        doc.save(file_stream)

        file_stream.seek(0)

        return file_stream.read()