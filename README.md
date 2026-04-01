# 📄 SoLicita — Assistente Inteligente para Licitações Públicas

O **SoLicita** é uma aplicação que automatiza a geração de **Termos de Referência (TR)** com base na **Lei 14.133/2021**, utilizando **RAG (Retrieval-Augmented Generation)** e modelos de linguagem (LLMs).

O sistema foi projetado para gerar documentos técnicos **consistentes, padronizados e adaptáveis**, reduzindo o esforço manual na elaboração de processos licitatórios.

É importante salientar que a estrutura do termo de referência varia de município para município. Mesmo assim, a aplicação ja trabalha para atender os diferentes modelos, contanto que os campos simulados estejam configurados no template.

---

## 🚀 Principais Funcionalidades

### 📄 Geração Automatizada de TR

- Geração completa de Termo de Referência em `.docx`
- Estrutura modular por seções
- Conteúdo adaptado ao contexto da contratação
- Uso de documentos institucionais e legislação como base

### 🧠 RAG (Retrieval-Augmented Generation)

- Consulta a:
  - 📚 Leis (ex: Lei 14.133/2021)
  - 📄 Modelos institucionais
- Recuperação semântica com embeddings
- Geração baseada em contexto real (menos alucinação)

### 🧩 Arquitetura Orientada a Seções

- Cada seção do TR é gerada individualmente
- Prompts especializados por contexto
- Maior controle sobre qualidade e coerência

---

## 🧠 Como o Sistema Funciona

O fluxo da aplicação segue uma arquitetura baseada em RAG + geração estruturada:

O funcionamento do sistema segue as seguintes etapas:

1. O usuário preenche o formulário na interface (Streamlit).1
2. A aplicação recebe os dados e chama a função generate_tr
3. O sistema percorre cada seção do Termo de Referência
4. Para cada seção:
    - Realiza uma busca no banco vetorial (Chroma)
    - Recupera contextos relevantes (leis e modelos)
    - Envia o contexto junto com os dados para o modelo de linguagem (LLM)
    - Gera o conteúdo da seção
5. Todas as seções geradas são inseridas no template .docx
6. O documento final é gerado e disponibilizado para download

### Etapas:

1. Usuário fornece dados da contratação
2. O sistema percorre cada seção do TR
3. Para cada seção:
   - Busca contexto relevante (RAG)
   - Gera conteúdo com LLM
4. O documento final é montado com `docxtpl`

---

## 🏗️ Arquitetura do Projeto

```
.
├── app.py              # Orquestra geração do TR
├── interface.py        # Interface Streamlit
├── ingest.py           # Pipeline de ingestão (RAG)
├── pipeline.py         # Pipeline de geração (LLM + Prompt)
├── vectorstore.py      # Carregamento do banco vetorial
├── prompts.py          # Templates de prompt
├── config.py           # Configurações globais
│
├── templates/          # Template .docx do TR
├── data/               # Documentos institucionais (RAG)
│   ├── laws/
│   └── tr_models/
│
├── vector_db/          # Banco vetorial persistido (Chroma)
└── requirements.txt
```

---

## 🔍 Detalhes Técnicos

### 🔹 Ingestão de Dados (`ingest.py`)

- Suporte a:
  - PDF (`PyPDFLoader`)
  - DOCX (`Docx2txtLoader`)
- Estratégias de chunking:
  - 📜 Leis → separação por artigos
  - 📄 Modelos → separação por seções
- Armazenamento:
  - ChromaDB (persistente)

---

### 🔹 Pipeline de Geração (`pipeline.py`)

- Modelo: `gpt-4o-mini`
- Baixa temperatura → maior precisão técnica
- Prompt estruturado por seção
- Uso de `LangChain` para orquestração

---

### 🔹 Geração do Documento (`app.py`)

- Loop por seções do TR
- Recuperação contextual (RAG)
- Geração independente por seção
- Renderização com `docxtpl`

---

### 🔹 Interface (`interface.py`)

- Streamlit
- Formulário estruturado
- Download direto do arquivo gerado
- Cache do vectorstore para performance

---

## 📁 Estrutura de Dados (RAG)

A pasta `data/` contém documentos utilizados como base de conhecimento.

⚠️ **Importante:**  
Os arquivos reais não estão no repositório por conterem dados sensíveis.

### Estrutura esperada:

```
data/
├── laws/         # Leis e normas
├── tr_models/    # Modelos institucionais reais
```

### Exemplo de modelo:

```
1. OBJETO
Conteúdo...

2. JUSTIFICATIVA
Conteúdo...

3. EXECUÇÃO
Conteúdo...
```

---

## ⚙️ Instalação

```bash
git clone https://github.com/c-machad0/bidding_assistant.git

cd bidding_assistant

python -m venv venv

# Windows
venv\Scripts\activate

pip install -r requirements.txt
```

---

## ▶️ Execução

```bash
streamlit run interface.py
```

---

## 🔐 Variáveis de Ambiente

Crie um arquivo `.env` ou configure no sistema:

```
OPENAI_API_KEY=sua-chave-aqui
```

---

## 📌 Roadmap

- [x] Geração de TR por seções
- [x] Integração com RAG
- [x] Exportação em `.docx`
- [ ] Interface mais robusta (validações e UX)
- [ ] Multi-modelos de TR por município
- [ ] Histórico de documentos gerados
- [ ] Deploy (Streamlit Cloud ou backend dedicado)
- [ ] Controle de versões dos documentos

---

## 💡 Diferenciais do Projeto

- Arquitetura **modular e escalável**
- Uso real de **RAG aplicado ao setor público**
- Separação clara de responsabilidades
- Foco em **problema real de negócio**
- Pronto para evolução como produto SaaS

---

## 🤝 Contribuição

1. Fork o projeto  
2. Crie uma branch (`feature/minha-feature`)  
3. Commit suas alterações  
4. Abra um Pull Request  

---

## 📄 Licença

MIT License

---

## 👨‍💻 Autor

Desenvolvido por **Christian Machado**
