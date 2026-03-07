import streamlit as st

st.header("Gerar Termo de Referência", text_alignment="center")

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
        st.text_input("Justificativa")
        st.text_input("Prazo de Execução")
        st.text_input("Modalidade")

        button = st.form_submit_button("Gerar")