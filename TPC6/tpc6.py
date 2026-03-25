import spacy
from spacy.matcher import Matcher

nlp=spacy.load("pt_core_news_lg")
texto = open("C:\\Users\\barba\\OneDrive - Universidade do Minho\\Universidade\\4ºano\\2º Semestre\\PLN\\Repositório Professor\\Dados\\Harry Potter e A Pedra Filosofal.txt", encoding="utf-8")
texto = texto.read()
doc = nlp(texto)
amigos={}
for sent in doc.sents: #.sents separa o texto em sentenças.
    amigo=[]
    for entity in sent.ents: #.ents identifica as entidades nomeadas.
        if entity.label_ == "PER":
            if entity.text not in amigo:
                amigo.append(entity.text)
    if len(amigo)>1:
        for w in amigo:
            for w2 in amigo:
                if w!=w2:
                    if w not in amigos:
                        amigos[w]={}    
                    if w2 not in amigos[w]:
                        amigos[w][w2]=1
                    else:
                            amigos[w][w2]+=1

print(amigos)