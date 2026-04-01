# 📂 templates/

A pasta `templates/` contém o arquivo `.docx` utilizado como template base para geração do Termo de Referência final.

## Função

- Define a estrutura final do documento
- Utiliza a biblioteca `docxtpl` para renderização dinâmica
- Permite a substituição de placeholders pelos conteúdos gerados automaticamente

## Exemplo de placeholders

```
{{objeto}}
{{fundamentação}}
{{execução}}
```

Cada placeholder corresponde a uma seção gerada pela aplicação.

## Observação

Para o correto funcionamento:

- Os nomes das seções devem ser compatíveis com a lista definida em `config.py`
- Os placeholders no template devem corresponder exatamente às chaves utilizadas na aplicação
