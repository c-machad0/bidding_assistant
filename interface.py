from datetime import date


import streamlit as st


from app import App


@st.cache_resource
def load_engine():
    app = App()

    return app

app = load_engine()

st.set_page_config(
            page_title='SoLicita',
            page_icon='📄',
        )

st.header("Bem vindo ao SoLicita", text_alignment="center")
st.subheader("Seu assistente de licitações.", text_alignment="center")

# with st.sidebar:
#     st.file_uploader(
#         label="Faça upload do(s) arquivo(s)",
#         type=['.pdf', '.docx'],
#         accept_multiple_files=True
#     )

with st.form("Geração de Termo de Referência"):
        objeto_tr = st.text_input("Resumo do objeto")
        select_secretary = st.selectbox(
            label="Secretaria solicitante",
            options=[
                "Secretaria de Educação",
                "Secretaria de Esporte e Lazer",
                "Secretaria de Cultura",
                "Secretaria de Administração",
                "Secretaria de Desenvolvimento Social",
                "Secretaria de Desenvolvimento Urbano",
            ]
        )
        date_execution = st.date_input(
                "Prazo de Execução",
                value=(date(2026, 1, 1), date(2030, 12, 31)),
                format="DD/MM/YYYY"
                )
        bidding_modality = st.selectbox(
             label="Modalidades",
             options=[
                "Dispensa de Licitação",
                "Pregão Eletrônico",
                "Pregão Presencial",
                "Concorrência Pública",
                "Inexigibilidade",
                "Credenciamento"
             ]
        )
        base_value = st.text_input("Valor médio da cotação")

        submitted = st.form_submit_button("Gerar")

        if submitted:
            with st.spinner("Gerando arquivo..."):
                app.generate_tr({
                "objeto_tr": objeto_tr,
                "select_secretary": select_secretary,
                "date_execution": date_execution,
                "bidding_modality": bidding_modality,
                "base_value": base_value
            })