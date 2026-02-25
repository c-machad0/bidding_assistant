import streamlit as st
from service import Service

@st.cache_resource # Decorator para armazenar em cache funções que retornam objetos de recursos (por exemplo, conexões de banco de dados, modelos de aprendizado de máquina).
def load_service():
    service = Service()
    service.build_service()
    
    return service

def home():
    st.header("Página Inicial")
    st.write("Bem-vindo ao sistema.")

def tr_generate():
    st.header('Gere seu termo de referência')

    uploaded_pdf = st.file_uploader(
        label='Selecione o(s) arquivo(s)',
        type=['pdf'],
        accept_multiple_files=True
    )

st.set_page_config(
    page_title='SoLicita',
    page_icon='📄',
    menu_items={

    }
)

if "page" not in st.session_state:
    st.session_state.page = "Home"

with st.sidebar:
    st.header("Menu")

    if st.button("Home"):
        st.session_state.page = "Home"

    if st.button("Gerar Termo de Referência"):
        st.session_state.page = "TR"

if st.session_state.page == "Home":
    home()

elif st.session_state.page == "TR":
    tr_generate()

service = load_service()

user_question = st.text_area(
    'Descreva detalhadamente sua dúvida ou solicitação técnica',
    height=200
)
button = st.button("Consultar")

if button and user_question.strip():
    with st.spinner("Consultando o banco de dados..."):
        response = service.rag_chain.invoke(user_question)
        st.markdown(response)
        st.divider()
