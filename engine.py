from rag_pipeline import RagPipeline
from prompts import CHAT_SYSTEM_PROMPT


class AIEngine(RagPipeline):


    def build_service(self):
        self.set_vector_store()
        self.retriever_vector_store()

    
    def ask_question(self, question):
        self.set_user_prompt(CHAT_SYSTEM_PROMPT)

        return self.set_rag_chain().invoke(question)
    

    def generate_tr(self):
        ...

    
    def generate_dfd(self):
        ...


if __name__ == "__main__":
    service = AIEngine()
    service.build_service()

    user_question = 'Quero fazer uma dispensa para contratação de serviços de dedetização para as escolas do município. Qual inciso eu uso?'

    response = service.ask_question(user_question)

    print(response)