# Extração de Redes de Personagens em Obras Literárias (TPC6)

Este projeto implementa um sistema de extração de relações entre personagens utilizando Processamento de Linguagem Natural (PLN). O foco principal é a análise da obra "Harry Potter e a Pedra Filosofal" para identificar co-ocorrências de entidades nomeadas e mapear o grafo de interações sociais da narrativa.

## Explicação do Código

A lógica de processamento deste script baseia-se em cinco etapas fundamentais para a extração de relações entre entidades:

### 1. Carregamento do Modelo
O comando `spacy.load("pt_core_news_lg")` carrega o modelo estatístico de alta densidade para a língua portuguesa. Este modelo é essencial pois contém o motor de **Reconhecimento de Entidades Nomeadas (NER)** treinado para identificar categorias complexas em textos extensos.

### 2. Processamento (Pipeline)
Ao instanciar `doc = nlp(texto)`, o spaCy executa automaticamente um pipeline que inclui:
* **Tokenização:** Segmentação do texto em unidades mínimas.
* **Sentencizer:** Divisão do texto em frases individuais.
* **Identificação de Entidades:** Localização e classificação de nomes próprios, locais e organizações.

### 3. Segmentação por Sentenças
O ciclo `for sent in doc.sents` define a unidade de contexto da análise. A premissa lógica do algoritmo assume que, se dois personagens são mencionados dentro da mesma frase, existe uma interação ou relação direta entre eles no contexto da narrativa.

### 4. Extração de Entidades (PER)
Dentro de cada frase, o código isola exclusivamente as entidades rotuladas como **"PER"** (Personagens/Pessoas). Os nomes são armazenados numa lista temporária designada `amigo`, sendo implementada uma verificação para evitar que a menção múltipla do mesmo personagem na mesma frase distorça a contagem de relações.

### 5. Construção da Matriz de Co-ocorrência
Para as sentenças que contêm mais do que um personagem (`len(amigo) > 1`), o script executa o mapeamento de adjacência:
* **Estrutura de Dados:** Utiliza um dicionário de dicionários (`amigos[w][w2]`) para representar uma matriz de adjacência dinâmica.
* **Incremento de Relações:** Sempre que dois personagens coabitam uma frase, o script incrementa o valor da relação em $+1$. Por exemplo, se "Harry" e "Ron" aparecem juntos, o peso da ligação entre ambos é atualizado bidirecionalmente (Harry para Ron e Ron para Harry).

