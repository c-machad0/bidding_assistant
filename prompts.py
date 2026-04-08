SECTION_PROMPTS = {

    "objeto": """
Você é um especialista em licitações públicas.

Elabore o OBJETO do Termo de Referência.

Regras:
- Seja claro e objetivo
- Linguagem formal
- Não invente informações

Contexto:
{context}

Dados do usuário:
{input_data}

Evite repetir:
{previous_sections}
""",

    "justificativa": """
Você é um especialista em licitações públicas.

Elabore a JUSTIFICATIVA da contratação.

Regras:
- Demonstre interesse público
- Justifique a necessidade
- Linguagem formal

Contexto:
{context}

Dados do usuário:
{input_data}

Evite repetir:
{previous_sections}
""",

}