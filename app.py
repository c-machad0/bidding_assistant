import streamlit as st
from rag_pipeline import RagPipeline
from engine import AIEngine

st.set_page_config(
            page_title='SoLicita',
            page_icon='📄',
        )

@st.cache_resource # Decorator para armazenar em cache funções que retornam objetos de recursos (por exemplo, conexões de banco de dados, modelos de aprendizado de máquina).
def load_engine():
    engine = AIEngine()
    engine.build_service()

    return engine

engine = load_engine()


home_page = st.Page(
    page="pages/home_page.py",
    title="Home",
    icon="🏠"
)

chat_page = st.Page(
    page="pages/chat_page.py",
    title="Chat",
    icon="💬"
    )
 

tr_page = st.Page(
    page="pages/tr_page.py",
    title="Gerar Termo de Referência",
    icon="📄"
    )

dfd_page = st.Page(
    page="pages/dfd_page.py",
    title="Gerar Documento de Formalização de Demanda",
    icon="📄"
    )

with st.sidebar:
    pages = st.navigation([
        home_page,
        chat_page, 
        tr_page, 
        dfd_page
        ])


pages.run()