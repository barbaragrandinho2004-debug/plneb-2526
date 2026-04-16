from flask import Flask, render_template, request
import json

app = Flask(__name__)

f_db = open(r"C:\Users\barba\OneDrive - Universidade do Minho\Universidade\4ºano\2º Semestre\PLN\plneb-2526\Exercícios\Aula3\dicionario_medico.json", 'r', encoding='utf-8')
db = json.load(f_db)

@app.get("/")
def home_page():
    return render_template("home.html")

@app.get("/conceitos")
def listar_conceitos():
    return render_template("conceitos.html", conceitos = db.keys())

@app.get("/conceitos/<designacao>")
def conceito(designacao):
    if designacao in db:
        descricao = db[designacao]
        return render_template("conceito.html", designacao = designacao, descricao = descricao)
    else:
        return render_template("erro.html", erro = "O conceito introduzido não existe")

@app.get("/api/conceitos")
def conceitos_api():
    return db

@app.get("/tabela")
def tabela():
    return render_template("tabela.html", conceitos=db)

@app.post("/conceitos")
def adicionar_conceitos():
    descricao = request.form["descricao"]
    designacao = request.form["designacao"]
    db[designacao] = descricao
    f_out=open("bd.json","w")
    json.dump(db,f_out, indent=4, ensure_ascii=False)
    f_out.close()
    return render_template("conceitos.html", conceitos=db.keys())

@app.delete("/conceitos/<designacao>")
def apagar_conceito(designacao):
    del db[designacao]
    f_out=open("bd.json","w")
    json.dump(db,f_out, indent=4, ensure_ascii=False)
    f_out.close()
    return {"redirect_url":"/conceitos", "message":"Conceito apagado com sucesso!"}

@app.route("/pesquisar")
def pesquisar():
    query = request.args.get("query", "")
    case_sensitive = request.args.get("case_sensitive") == "on"
    word_boundary = request.args.get("word_boundary") == "on"
    
    resultados = []

    if query:
        for designacao, descricao in db.items():
            # Criamos cópias para comparação baseada na escolha de Case Sensitive
            target_desig = designacao if case_sensitive else designacao.lower()
            target_desc = descricao if case_sensitive else descricao.lower()
            search_query = query if case_sensitive else query.lower()

            encontrou = False

            if word_boundary:
                # Lógica de Word Boundary sem 're': 
                # Partimos o texto em palavras e verificamos a igualdade exata
                # (Limpamos pontuação básica para não falhar em "dor,")
                palavras_desig = target_desig.replace(',', ' ').replace('.', ' ').split()
                palavras_desc = target_desc.replace(',', ' ').replace('.', ' ').split()
                
                if search_query in palavras_desig or search_query in palavras_desc:
                    encontrou = True
            else:
                # Pesquisa simples (substring)
                if search_query in target_desig or search_query in target_desc:
                    encontrou = True

            if encontrou:
                # Para o bold, usamos replace (se não for case sensitive, o bold pode ser imperfeito)
                # No modo Case Sensitive, o replace funciona bem:
                desig_bold = designacao.replace(query, f"<b>{query}</b>")
                desc_bold = descricao.replace(query, f"<b>{query}</b>")

                resultados.append({
                    "designacao": designacao,
                    "desig_label": desig_bold,
                    "descricao": desc_bold
                })

    return render_template("pesquisar.html", resultados=resultados, query=query, case_sensitive=case_sensitive, word_boundary=word_boundary)

app.run(host="localhost", port=4002, debug=True)