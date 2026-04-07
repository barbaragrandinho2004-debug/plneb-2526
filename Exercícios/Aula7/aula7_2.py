from flask import Flask, json, render_template

app = Flask(__name__)

f_db=open("C:\\Users\\barba\\OneDrive - Universidade do Minho\\Universidade\\4ºano\\2º Semestre\\PLN\\plneb-2526\\Exercícios\\Aula3\\dicionario_medico.json", encoding="utf-8")
db=json.load(f_db)

@app.get ("/")
def home_page():
    return render_template ("home.html")

@app.get ("/conceitos")
def listar_conceitos():
    return render_template ("conceitos.html", conceitos=db.keys())

@app.get ("/conceitos/<designacao>")
def conceito(designacao):
    if designacao in db:
        descricao=db[designacao] 
        return render_template ("conceito.html", designacao=designacao, descricao=descricao)
    else:
        return render_template ("erro.html", erro="Conceito introduzido não foi encontrado")

@app.get("/api/conceitos")
def conceitos_api():
    return db

app.run(host="localhost", port=4002, debug=True)