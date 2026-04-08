from io import BytesIO

from config import sections, get_template
from docxtpl import DocxTemplate
from pipeline import RagPipeline


class App():

    def __init__(self, vectorstore):
        self.rag = RagPipeline(vectorstore)

    
    def generate_tr(self, data):

        result = {}
        previous_sections = ""

        objeto_tr = data["objeto_tr"]
        select_secretary = data["select_secretary"]
        start_date = data["start_date"]
        end_date = data["end_date"]
        bidding_modality = data["bidding_modality"]
        base_value = data["base_value"]

        template_path = get_template()
        doc = DocxTemplate(template_path)

        # tratar datas
        start_date_str = start_date.strftime("%d/%m/%Y")
        end_date_str = end_date.strftime("%d/%m/%Y")

        for section in sections:

            response = self.rag.generate_section(
                section=section,
                data={
                    "objeto_tr": objeto_tr,
                    "select_secretary": select_secretary,
                    "start_date": start_date_str,
                    "end_date": end_date_str,
                    "bidding_modality": bidding_modality,
                    "base_value": base_value,
                },
                previous_sections=previous_sections
            )

            result[section] = response
            previous_sections += f"\n{response}"

        # ✅ adicionar datas no template corretamente
        result["start_date_str"] = start_date_str
        result["end_date_str"] = end_date_str

        doc.render(result)

        file_stream = BytesIO()
        doc.save(file_stream)

        file_stream.seek(0)

        return file_stream.read()