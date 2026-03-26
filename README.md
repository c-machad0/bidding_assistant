# 📄 SoLicita - Assistente de Licitações

O **SoLicita** é uma aplicação desenvolvida para auxiliar na elaboração de documentos licitatórios, com foco na **geração automatizada de Termos de Referência (TR)**.

A aplicação utiliza modelos de linguagem (LLMs) para gerar documentos estruturados, organizados por seções e adaptáveis conforme o contexto da contratação.

---

## 🚀 Funcionalidades

### 📄 Geração de Termo de Referência (TR)

- Geração automatizada de TR completo
- Estrutura dividida por seções
- Uso de prompts específicos para cada parte do documento
- Maior controle e consistência no conteúdo gerado
- Facilidade de adaptação para diferentes tipos de contratação

---

## 🧠 Como funciona

A geração do Termo de Referência segue um fluxo estruturado:

1. O usuário fornece as informações necessárias sobre o objeto da contratação
2. O sistema divide o documento em seções lógicas
3. Cada seção é gerada individualmente utilizando prompts específicos
4. As seções são consolidadas em um documento final coeso

Essa abordagem permite maior controle sobre a qualidade e padronização do documento.

---

## 🗂️ Estrutura do Projeto

A aplicação segue uma organização simples e funcional:

```
.
├── app.py                  # Lógica principal da aplicação
├── ingest.py               # Processo de RAG
├── data/                   # Arquivos de modelos institucionais
├── pipeline.py             # Pipeline e consumo dos arquivos ingeridos
├── prompts.py              # Modelos de prompts usados
├── interface.py            # Interface da aplicação
├── requirements.txt        # Dependências do projeto
```

---

## 🛠️ Tecnologias Utilizadas

- Python
- Streamlit
- LangChain
- OpenAI (LLM)

---

## ⚙️ Instalação

```bash
# Clone o repositório
git clone https://github.com/c-machad0/bidding_assistant.git

# Acesse a pasta
cd bidding_assistant

# Crie um ambiente virtual
python -m venv venv

# Ative o ambiente
# Windows
venv\Scripts\activate

# Instale as dependências
pip install -r requirements.txt
```

---

## ▶️ Execução

```bash
streamlit run .\interface.py
```

---

## 📌 Roadmap

- [x] Geração de TR por seções
- [x] Estrutura baseada em prompts específicos
- [ ] Exportação automática para Word (.docx)
- [ ] Interface mais detalhada para entrada de dados
- [ ] Persistência de documentos gerados
- [ ] Personalização por tipo de contratação

---

## 🤝 Contribuição

Contribuições são bem-vindas!

1. Fork o projeto
2. Crie uma branch (`feature/minha-feature`)
3. Commit suas alterações
4. Abra um Pull Request

---

## 📄 Licença

Este projeto está sob a licença MIT.

---

## 👨‍💻 Autor

Desenvolvido por **Christian Machado**
