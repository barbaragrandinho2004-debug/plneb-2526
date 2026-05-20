import spacy
import math

corpus = ["The sky is blue",
          "The sun is bright",
          "The sun in the sky"]

nlp = spacy.load("en_core_web_sm")

def limpar_corpus(corpus):
    """Pré-processa cada documento: tokeniza, converte para minúsculas e remove stop words e pontuação."""
    corpus_limpo = []
    for texto in corpus:
        doc_spacy = nlp(texto)
        tokens_validos = [
            token.text.lower()
            for token in doc_spacy
            if not token.is_stop and not token.is_punct
        ]
        corpus_limpo.append(tokens_validos)
    return corpus_limpo


def calcular_tf(tokens):
    """Calcula a Frequência Relativa (TF) de cada termo num documento."""
    total = len(tokens)
    contagens = {}
    for termo in tokens:
        contagens[termo] = contagens.get(termo, 0) + 1
    return {termo: freq / total for termo, freq in contagens.items()}


def calcular_idf(corpus_limpo):
    """Calcula o Inverse Document Frequency (IDF) para todos os termos do corpus."""
    num_docs = len(corpus_limpo)
    termos_globais = set(termo for doc in corpus_limpo for termo in doc)
    idf_map = {}
    for termo in termos_globais:
        docs_com_termo = sum(1 for doc in corpus_limpo if termo in doc)
        idf_map[termo] = math.log(num_docs / docs_com_termo, 10)
    return idf_map


def construir_matriz_tfidf(corpus_limpo):
    """Constrói a matriz TF-IDF: cada linha é o vetor de pesos de um documento."""
    idf_map = calcular_idf(corpus_limpo)
    vocabulario = sorted(idf_map.keys())
    matriz = []
    for doc in corpus_limpo:
        tf_doc = calcular_tf(doc)
        vetor = [
            tf_doc.get(termo, 0) * idf_map[termo]
            for termo in vocabulario
        ]
        matriz.append(vetor)
    return matriz


def similaridade_cosseno(vetor_a, vetor_b):
    """Calcula a Similaridade do Cosseno entre dois vetores."""
    produto_interno = sum(a * b for a, b in zip(vetor_a, vetor_b))
    magnitude_a = math.sqrt(sum(a ** 2 for a in vetor_a))
    magnitude_b = math.sqrt(sum(b ** 2 for b in vetor_b))
    return produto_interno / (magnitude_a * magnitude_b)


def pesquisar(query, vocabulario, idf_map, matriz):
    """Processa uma query e devolve os documentos ordenados por relevância."""
    # Pré-processar e vetorizar a query
    tokens_query = limpar_corpus([query])[0]
    tf_query = calcular_tf(tokens_query)
    vetor_query = [
        tf_query.get(termo, 0) * idf_map.get(termo, 0)
        for termo in vocabulario
    ]

    print(f"Vetor da query: {vetor_query}")

    # Calcular similaridade com cada documento e ordenar
    ranking = [
        (f"D{idx + 1}", similaridade_cosseno(vetor_query, vetor_doc))
        for idx, vetor_doc in enumerate(matriz)
    ]
    ranking.sort(key=lambda par: par[1], reverse=True)
    return ranking


# --- Execução principal ---
corpus_limpo = limpar_corpus(corpus)
idf_map = calcular_idf(corpus_limpo)
vocabulario = sorted(idf_map.keys())
matriz_tfidf = construir_matriz_tfidf(corpus_limpo)

print("--- Coleção ---")
print(corpus_limpo)
print("\n--- Matriz TF-IDF ---")
print(matriz_tfidf)

print("\n--- Resultado da query ---")
query = "The bright sun"
print(query)
resultados = pesquisar(query, vocabulario, idf_map, matriz_tfidf)
print(f"Ranking: {resultados}")
