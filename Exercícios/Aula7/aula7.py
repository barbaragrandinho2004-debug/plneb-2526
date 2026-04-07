import spacy

nlp = spacy.load("./models/model-best")

f = open("C:\\Users\\barba\\OneDrive - Universidade do Minho\\Universidade\\4ºano\\2º Semestre\\PLN\\Repositório Professor\\Dados\\Harry Potter e A Pedra Filosofal.txt", encoding="utf-8")
texto = f.read()

config={
    "overwrite_ents": True
}

doc = nlp(texto)

ruler = nlp.add_pipe("entity_ruler", last=True, config=config) #before, after, first

patterns = [
    {"label": "Pessoa", "pattern": "Dumbledore"}, 
    {"label": "Pessoa", "pattern": "Hagrid"}, 
    {"label": "Pessoa", "pattern": [{"LOWER": "albus"}, {"LOWER": "dumbledore"}]}, 
]

ruler.add_patterns(patterns)


doc = nlp(texto)

for ent in doc.ents:
    print(ent, ent.label_)