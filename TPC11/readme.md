# TPC 11

Neste TPC foi implementado um sistema base de Recuperação de Informação (IR) assente no Modelo de Espaço Vetorial, recorrendo ao algoritmo TF-IDF e à Similaridade do Cosseno para pontuar e ordenar documentos face a uma *query* de pesquisa.

## Funções Base

Para preparar o corpus e construir a matriz de pesos, foram implementadas as seguintes funções:

* **`limpar_corpus(corpus)`:** Utiliza a biblioteca `spaCy` (modelo `en_core_web_sm`) para processar cada texto. Extrai os *tokens*, converte-os para minúsculas e descarta *stop words* e sinais de pontuação através dos atributos `.is_stop` e `.is_punct`. Recorre a uma *list comprehension* para maior clareza e concisão.
* **`calcular_tf(tokens)`:** Calcula a Frequência Relativa (Term Frequency) de cada termo num documento. Usa `dict.get()` para contabilizar ocorrências sem necessidade de verificações explícitas, devolvendo um dicionário com a frequência relativa de cada termo.
* **`calcular_idf(corpus_limpo)`:** Calcula o *Inverse Document Frequency* para todos os termos do corpus. Constrói um conjunto de termos únicos globais e aplica a fórmula `math.log(N/DF, 10)`, penalizando termos comuns e valorizando os mais raros e distintivos.
* **`construir_matriz_tfidf(corpus_limpo)`:** Orquestra as métricas anteriores. Gera um vocabulário global ordenado alfabeticamente e produz a Matriz TF-IDF (lista de listas), em que cada vetor de documento contém o produto $TF \times IDF$ para cada termo do espaço dimensional. Usa *list comprehensions* tanto na construção do vocabulário como de cada vetor.

---

## Funções de Query e Cosseno

Para implementar o processamento da *query* e o cálculo do *ranking*, foram criadas as seguintes funções:

* **`similaridade_cosseno(vetor_a, vetor_b)`:** Calcula a Similaridade do Cosseno entre dois vetores. Recorre a `zip()` e *generator expressions* para calcular o produto interno e as magnitudes de forma compacta, dividindo o resultado pelo produto das duas magnitudes (`math.sqrt()`).
* **`pesquisar(query, vocabulario, idf_map, matriz)`:** Função principal do motor de busca. A execução divide-se nos seguintes passos:
  1. Aplica `limpar_corpus` à *query*, neste caso "The bright sun".
  2. Calcula o `calcular_tf` da *query* e projeta-o no espaço dimensional do vocabulário, cruzando esses valores com o `idf_map` já calculado para gerar o vetor da *query*.
  3. Compara o vetor obtido com todos os vetores da `matriz` através de `similaridade_cosseno`, construindo o *ranking* com uma *list comprehension*.
  4. Ordena os resultados com `.sort(key=lambda par: par[1], reverse=True)` e devolve o *Ranking* Final como lista de tuplos.
