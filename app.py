import os
from io import BytesIO


from config import BASE_DIR, sections
from docxtpl import DocxTemplate
from ingest import RagIngest
from pipeline import RagPipeline


class App():

    def __init__(self):
        self.rag = RagPipeline()

        if not os.path.exists("vector_db"): # verifica se o vector_db existe
            ingest = RagIngest()
            ingest.build_ingest()

    
    def generate_tr(self, data):

        result = {}

        objeto_tr = data["objeto_tr"]
        select_secretary = data["select_secretary"]
        date_execution = data["date_execution"]
        bidding_modality = data["bidding_modality"]
        base_value = data["base_value"]

        template_path = os.path.join(
            BASE_DIR,
            "modelo_tr_dispensa.docx"
        )

        doc = DocxTemplate(template_path)

        # tratar datas
        if isinstance(date_execution, tuple):
            start_date, end_date = date_execution
            date_execution_str = f"{start_date} a {end_date}"
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

        doc.render(result)

        file_stream = BytesIO()
        doc.save(file_stream)

        file_stream.seek(0)

        return file_stream.read()