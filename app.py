import streamlit as st
from rag_pipeline import RagPipeline
from engine import AIEngine

st.set_page_config(
            page_title='SoLicita',
            page_icon='📄',
            menu_items={

            }
        )

@st.cache_resource # Decorator para armazenar em cache funções que retornam objetos de recursos (por exemplo, conexões de banco de dados, modelos de aprendizado de máquina).
def load_engine():
    engine = AIEngine()
    engine.build_service()

    return engine

class App:
    
    def __init__(self):
        st.header("Bem vindo ao SoLicita")
        st.subheader("Seu assistente técnico de licitações.")

        self.tab_chat, self.tab_tr, self.tab_dfd = st.tabs([
            "Chat",
            "Gerar Termo de Referência",
            "Gerar Documento de Formalização de Demanda",
        ])

        self.engine = load_engine()
        

    def chose_tab(self):
        with self.tab_chat:
            self.ai_chat()

        with self.tab_tr:
            self.tr_field()

        with self.tab_dfd:
            self.dfd_field()


    def tr_field(self):
        with st.form("Geração de Termo de Referência"):
            st.text_input("Objeto")
            st.selectbox(
                label="Secretaria solicitante",
                options=[
                    "Secretaria de Educação",
                    "Secretaria de Esporte e Lazer",
                    "Secretaria de Cultura",
                    "Secretaria de Administração",
                    "Secretaria de Desenvolvimento Social",
                ]
            )
            st.text_area("Justificativa")
            st.text_input("Prazo de Execução")
            st.text_input("Modalidade")

            button = st.form_submit_button("Gerar")


    def dfd_field(self):
        with st.form("Geração de Documento de Formalização de Demanda"):
            st.text_input("Objeto")
            st.selectbox(
                label="Secretaria solicitante",
                options=[
                    "Secretaria de Educação",
                    "Secretaria de Esporte e Lazer",
                    "Secretaria de Cultura",
                    "Secretaria de Administração",
                    "Secretaria de Desenvolvimento Social",
                ]
            )
            st.text_area("Justificativa")
            st.text_input("Prazo de Execução")
            st.text_input("Modalidade")

            button = st.form_submit_button("Gerar")


    def ai_chat(self):
        user_question = st.chat_input("Como posso ajudar?")

        if "messages" not in st.session_state:
            st.session_state["messages"] = []

        if user_question and user_question.strip():
            for message in st.session_state.messages:
                st.chat_message(message["role"]).write(message["content"])

            st.chat_message("user").write(user_question)

            st.session_state.messages.append(
                {"role": "user", "content": user_question}
            )

            if user_question:
                with st.spinner('Buscando resposta...'):
                    response = self.engine.ask_question(user_question)

                    st.chat_message("assistant").write(response)

                    st.session_state.messages.append(
                        {"role": "assistant", "content": response}
                    )

app = App()
app.chose_tab()