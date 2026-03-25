import spacy

nlp = spacy.load("pt_core_news_lg")

texto=open("C:\\Users\\barba\\OneDrive - Universidade do Minho\\Universidade\\4ºano\\2º Semestre\\PLN\\Repositório Professor\\Dados\\Harry Potter e A Pedra Filosofal.txt", encoding="utf-8")
texto = texto.read()

doc = nlp(texto)

print("="*20, "Tokens", "="*20)

verbs={}
for token in doc:
    if token.pos_ in ["VERB", "AUX"]:
        #if token.text in verbs:
        if token.lemma_ in verbs:
            verbs[token.lemma_] += 1

        else:
            verbs[token.lemma_]=1


#def ordena(elem):
    #return elem[1] 

sorted_dict=sorted(verbs.items(), key=lambda x: x[1], reverse=True)

print("="*20, "Verbos mais frequentes", "="*20)
print(sorted_dict[:10])

        

