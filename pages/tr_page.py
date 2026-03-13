import streamlit as st
from datetime import date


st.header("Gerar Termo de Referência", text_alignment="center")

with st.form("Geração de Termo de Referência"):
        objeto_tr = st.text_input("Objeto")
        select_secretary = st.selectbox(
            label="Secretaria solicitante",
            options=[
                "Secretaria de Educação",
                "Secretaria de Esporte e Lazer",
                "Secretaria de Cultura",
                "Secretaria de Administração",
                "Secretaria de Desenvolvimento Social",
            ]
        )
        date_execution = st.date_input(
                "Prazo de Execução",
                value=(date(2026, 1, 1), date(2030, 12, 31)),
                format="DD/MM/YYYY"
                )
        bidding_modality = st.selectbox(
              label="Modalidade de Licitação",
              options=[
                    "Pregão Eletrônico",
                    "Pregão Presencial",
                    "Dispensa de Licitação",
                    "Inexigibilidade de Licitação",
                    "Concorrência",
                    "Credenciamento",
                    "Inexigibilidade de Licitação",
              ]
        )

        with st.spinner():
            button = st.form_submit_button("Gerar")