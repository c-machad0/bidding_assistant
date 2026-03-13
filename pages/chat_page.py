from engine import AIEngine
import streamlit as st

@st.cache_resource # Decorator para armazenar em cache funções que retornam objetos de recursos (por exemplo, conexões de banco de dados, modelos de aprendizado de máquina).
def load_engine():
    engine = AIEngine()

    return engine

engine = load_engine()

st.header("Chat - SoLicita", text_alignment="center")

if "messages" not in st.session_state:
    st.session_state["messages"] = []

# Mostra histórico
for message in st.session_state.messages:
    st.chat_message(message["role"]).write(message["content"])
        
# Mensagem do usuário
user_question = st.chat_input("Como posso ajudar?")

if user_question:
    # Mostra a pergunta
    st.chat_message("user").write(user_question)

    st.session_state.messages.append(
        {"role": "user", "content": user_question}
    )

    # Gera a resposta
    with st.spinner('Buscando resposta...'):
        response = engine.ask_question(user_question)

        st.chat_message("assistant").write(response)

        st.session_state.messages.append(
            {"role": "assistant", "content": response}
        )