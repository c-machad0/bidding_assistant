import os


from rag.ingest import RagIngest
from rag.rag_pipeline import RagPipeline


class AIEngine():

    def __init__(self):
        self.rag = RagPipeline()

        if not os.path.exists("vector_db"): # verifica se o vector_db existe
            ingest = RagIngest()
            ingest.build_ingest()


    def ask_question(self, question):
        return self.rag.chat_chain.invoke(question)
    

    def generate_tr(self):
        ...


if __name__ == "__main__":
    service = AIEngine()
    service.ask_question()

    user_question = 'Quero fazer uma dispensa para contratação de serviços de dedetização para as escolas do município. Qual inciso eu uso?'

    response = service.ask_question(user_question)

    print(response)