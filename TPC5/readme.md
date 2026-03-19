# TPC5
# Web Scraping e Estruturação de Dados: Portal Atlas da Saúde

## 1. Introdução
O objetivo central é a criação de um script de recolha automática de dados (web scraping) capaz de extrair definições e descrições detalhadas de patologias do portal "Atlas da Saúde". O resultado final é um dataset estruturado em formato JSON, otimizado para futuras tarefas de mineração de texto ou análise linguística.

## 2. Metodologia e Implementação

O script utiliza uma abordagem de extração em dois níveis para garantir a máxima densidade de informação por cada entrada.

### 2.1. Navegação Alfabética
Para garantir a cobertura total do diretório de doenças, o script utiliza a biblioteca `string` para iterar sobre todos os caracteres do abecedário português (`ascii_lowercase`). Esta abordagem permite construir dinamicamente os URLs de índice (ex: `.../doencasAaZ/a`, `.../doencasAaZ/b`), contornando limitações de paginação simples.

### 2.2. A Função de Extração (`extrair_pagina`)
A lógica principal está encapsulada nesta função, que processa cada página de índice da seguinte forma:

1. **Localização de Entradas:** Utiliza o seletor `soup.find_all("div", class_="views-row")` para isolar cada bloco de doença.
2. **Captura de Metadados de Superfície:** Extrai o nome da patologia (designação) e o resumo breve que consta na listagem geral.
3. **Deep Scraping (Extração Profunda):** Identifica o link (`href`) para a página detalhada da doença. É realizado um segundo pedido HTTP (`requests.get`) para este URL específico, onde o script isola a `div` de classe `field-name-body` para recuperar o texto científico integral.

### 2.3. Agregação e Estruturação de Dados
Os dados são armazenados num dicionário Python. Para a fusão dos resultados de cada letra, foi utilizado o operador de união de dicionários (`|`), introduzido no Python 3.9, que permite uma junção eficiente e legível das coleções de dados:
`res = res | extrair_pagina(url+letra)`

## 3. Especificações Técnicas

### Dependências
* **Requests:** Gestão de sessões HTTP e recuperação do código-fonte.
* **BeautifulSoup4:** Parsing do DOM (Document Object Model) e extração de elementos via seletores.
* **JSON:** Serialização dos dados para formato persistente.

### Tratamento de Caracteres e Encoding
Dada a natureza da língua portuguesa, o ficheiro de saída é gerado com `encoding="utf8"` e o parâmetro `ensure_ascii=False`. Esta configuração é crítica para que os caracteres acentuados e cedilhas sejam preservados no ficheiro JSON, evitando a conversão para sequências Unicode ilegíveis por humanos.

## 4. Estrutura do Output

O ficheiro `doencasTPC.json` resultante segue o seguinte esquema de dicionário aninhado:

```json
{
    "Nome da Doença": {
        "small_descs": "Resumo inicial da listagem",
        "full_desc": "Texto completo extraído da página de detalhe"
    }
}
```

## 5. Instruções de Execução

1. Instalar as dependências necessárias:
`pip install beautifulsoup4 requests`

2. Executar o script:
`python tpc5.py`

3. Verificar o ficheiro gerado doencasTPC.json na diretoria atual.