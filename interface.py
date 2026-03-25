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
st.subheader("Seu assistente de licitações", text_alignment="center")

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
        start_date = st.date_input(
                "Data de elaboração do Termo de Referência",
                value=date(2026, 1, 1),
                format="DD/MM/YYYY"
                )
        
        end_date = st.date_input(
            "Vigência do contrato",
            value=date(2027, 12, 31),
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
        file_bytes = app.generate_tr({
        "objeto_tr": objeto_tr,
        "select_secretary": select_secretary,
        "start_date": start_date,
        "end_date": end_date,
        "bidding_modality": bidding_modality,
        "base_value": base_value
        })

        if not file_bytes:
            st.error("Erro ao gerar o arquivo.")
        else:
            st.session_state["file_bytes"] = file_bytes
            st.success("Termo de Referência gerado com sucesso!")

        
        if 'file_bytes' in st.session_state:
            st.download_button(
                label="Download Termo de Referência",
                data=file_bytes,
                file_name="novo_tr.docx",
                key='download_tr',
            )