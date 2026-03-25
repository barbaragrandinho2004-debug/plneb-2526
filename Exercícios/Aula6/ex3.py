import spacy
from spacy.matcher import Matcher

#o spacy é uma biblioteca de processamento de linguagem natural (PLN) que me permite analisar e extrair informações de textos em português. O Matcher é uma classe do spaCy que me permite definir padrões de correspondência para encontrar sequências específicas de tokens no texto, como verbos seguidos de substantivos, por exemplo.
nlp = spacy.load("pt_core_news_lg") #carregar o modelo de linguagem em português, que é necessário para processar o texto e extrair as informações linguísticas relevantes para a análise dos verbos. O modelo "pt_core_news_lg" é um modelo pré-treinado que contém informações sobre a gramática, sintaxe e semântica da língua portuguesa, o que me permite identificar os verbos e suas formas corretas (lemas) no texto.

texto=open("C:\\Users\\barba\\OneDrive - Universidade do Minho\\Universidade\\4ºano\\2º Semestre\\PLN\\Repositório Professor\\Dados\\Harry Potter e A Pedra Filosofal.txt", encoding="utf-8")
texto = texto.read()

doc = nlp(texto) #o doc é um objeto que contém o texto processado, com todas as informações linguísticas associadas a cada token, como a sua forma original, lema, categoria gramatical, dependências sintáticas, etc. É o que me permite iterar sobre os tokens

matcher = Matcher(nlp.vocab)

pattern = [{"ENT_TYPE": "PER"},
           {"POS": {"IN": ["AUX", "VERB"]}, "OP" : "+"},
           {"POS": "DET", "OP" : "?"},
           {"POS": "NOUN"}]

matcher.add("match_id", [pattern])
matches = matcher(doc)

for id, start, end in matches: #o método matcher retorna uma lista de tuplos em que o primeiro elemento é o id do padrão e os outros dois são as posições de início e fim do trecho que corresponde ao padrão
    print(doc[start:end]) #o que estou a fazer aqui é imprimir o trecho do texto que corresponde ao padrão encontrado, usando as posições de início e fim para extrair a parte relevante do doc

print(len(matches))
#lista de tuplos em que o primeiro elemento é o id do padrão e os outros dois são as posições de início e fim do trecho que corresponde ao padrão