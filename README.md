# 📄 SoLicita – Assistente Técnico de Licitações

**SoLicita** é um assistente técnico de apoio à elaboração de processos licitatórios e análise de matéria normativa, fundamentado na **Lei 14.133/2021** e em modelos institucionais internos. O objetivo é auxiliar servidores públicos na interpretação de dispositivos legais e no embasamento técnico de suas decisões.

> ⚠️ **Este projeto está apenas começando** e se encontra em fase de desenvolvimento contínuo. Novas funcionalidades, ajustes de base legal e melhorias de interface serão incorporadas ao longo do tempo.

## 🧩 O que a aplicação faz

- **Consulta rápida à legislação de licitações (Lei 14.133/2021)** via RAG (Retrieval-Augmented Generation).
- **Respostas técnicas** com referência ao artigo, parágrafo e inciso sempre que possível.
- **Interface simples e amigável** para servidores, sem necessidade de conhecimento avançado em tecnologia.
- Base de dados local persistente com `Chroma` e `LangChain`, permitindo consultas rápidas a trechos específicos da lei.

## 🚀 Status atual

O sistema atualmente:

- Carrega o PDF da Lei 14.133/2021.
- Segmenta o conteúdo por artigos e chunks.
- Armazena vetores em um banco local (`Chroma`).
- Oferece um chat simples via `Streamlit` para perguntas sobre dispensa de licitação, tipos de licitação, requisitos e situações típicas de contratações públicas.

Este é um **protótipo funcional** que está sendo iterado a partir de uso real e ajustes normativos.

## ⚙️ Tecnologias utilizadas

- **Python 3.9+**
- **LangChain** (Core + OpenAI + Chroma + Splitters)
- **Chroma** como vector store local
- **OpenAI + GPT‑4o‑mini** para geração de respostas
- **Streamlit** para interface web simples
- **PyPDFLoader** para leitura do PDF da Lei 14.133/2021

## 📦 Como instalar e rodar

1. Clone o repositório:

```bash
git clone https://github.com/c-machad0/bidding_assistant.git
cd bidding_assistant
