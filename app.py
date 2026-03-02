import streamlit as st
from service import Service

@st.cache_resource # Decorator para armazenar em cache funções que retornam objetos de recursos (por exemplo, conexões de banco de dados, modelos de aprendizado de máquina).
def load_service():
    service = Service()
    service.build_service()
    
    return service


st.header("Bem vindo ao SoLicita")
st.subheader("Seu assistente sobre licitações.")

st.set_page_config(
    page_title='SoLicita',
    page_icon='📄',
    menu_items={

    }
)

service = load_service()

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
            response = service.ask_question(user_question)

            st.chat_message("assistant").write(response)

            st.session_state.messages.append(
                {"role": "assistant", "content": response}
            )