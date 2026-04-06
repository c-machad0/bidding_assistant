import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))


sections = [
    "objeto",
    "fundamentação",
    "solução",
    "bem_comum",
    "requisitos",
    "execução",
    "ob_contratante",
    "ob_contratada",
    "subcontratação",
    "secretaria",
    "start_date_str",
    "end_date_str",
]


def get_api_key():
    api_key = os.getenv("OPENAI_API_KEY")

    if not api_key:
        raise RuntimeError("OPENAI_API_KEY não configurada")

    return api_key

def get_template():
    template_path = os.getenv("TEMPLATE_PATH")

    if template_path:
        return os.path.join(BASE_DIR, template_path)

    return os.path.join(BASE_DIR, "templates", "modelo_tr.docx")