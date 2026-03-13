import streamlit as st


st.set_page_config(
            page_title='SoLicita',
            page_icon='📄',
        )

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


with st.sidebar:
    pages = st.navigation([
        home_page,
        chat_page, 
        tr_page, 
        ])


pages.run()