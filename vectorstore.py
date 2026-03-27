import streamlit as st


from langchain_community.vectorstores import Chroma
from langchain_openai import OpenAIEmbeddings


@st.cache_resource
def load_vectorstore():
    return Chroma(
        persist_directory='vector_db',
        embedding_function=OpenAIEmbeddings()
    )