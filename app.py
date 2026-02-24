import streamlit as st
from service import Service

@st.cache_resource # Decorator para armazenar em cache funções que retornam objetos de recursos (por exemplo, conexões de banco de dados, modelos de aprendizado de máquina).
def load_service():
    service = Service()
    service.build_service()
    
    return service

st.set_page_config(
    page_title='SoLicita',
    page_icon='📄',
    menu_items={

    }
)

st.header('Assistente Técnico de Licitações')
st.subheader('Fundamentado na Lei 14.133/2021 e modelos institucionais')
st.write('Ferramenta de apoio técnico. A responsabilidade final permanece do servidor responsável.')

with st.sidebar:
    st.sidebar.header("Informações do Sistema")
    st.sidebar.markdown("Base normativa: Lei 14.133/2021"
                        "\nModelos institucionais internos\n"
                        "\nVersão 1.0 (uso interno)"
                        )

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
