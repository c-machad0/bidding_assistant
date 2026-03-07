import streamlit as st
from app import load_engine


engine = load_engine()

st.header("Bem vindo ao SoLicita", text_alignment="center")
st.subheader("Seu assistente técnico de licitações.", text_alignment="center")