from flask import Flask, render_template
import json

app=Flask(__name__)

fd_b=open("C:\\Users\\barba\\OneDrive - Universidade do Minho\\Universidade\\4ºano\\2º Semestre\\PLN\\plneb-2526\\Exercícios\\Aula3\\dicionario_medico.json", encoding="utf-8")
db=json.load(fd_b)


# No teu aula_7.py, altera para:

@app.get("/")  #rota para humanos
def homepage():
    # Obtém o número total de conceitos no dicionário
    num_conceitos = len(db) 
    # Passa o valor para o template como 'num_conceitos'
    return render_template("home.html", num_conceitos=num_conceitos)

@app.get("/api/conceitos")  #rota para máquina
def conceitos_api():
    return db

@app.get("/conceitos")  
def conceitos():
    return render_template("conceitos.html", conceitos=db.keys())


@app.get("/conceitos/<designacao>")  #link variável
def conceito(designacao):
    if designacao in db:
        descricao = db[designacao]
        return render_template("conceito.html", designacao=designacao, descricao=descricao)
    else:
        return render_template("erro.html", error="O conceito introduzido não existe.")

app.run(host="localhost", port=4002, debug=True)