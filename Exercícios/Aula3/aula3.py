#ler ficheiro txt

from fileinput import filename
import re
f=open("dicionario_medico.txt","r", encoding="utf-8") #encoding="utf-8"
texto=f.read()
#limpar o texto

texto=re.sub(r"\f", "", texto) #substituir form feed por vazio #primeiro parametro o que quero substituir, segundo parametro pelo que vou substituir, terceiro parametro o texto onde quero fazer a substituição

#marcar conceitos

texto=re.sub(r"\n\n", "\n\n@", texto) #substituir duplo enter por duplo enter seguido de @


print(texto)

#capturar conceitos

conceitos_designacao=re.split(r"\n\n@", texto)
print(len(conceitos_designacao))

 
#encontrar todas as ocorrências de @ seguido de qualquer coisa que não seja um enter, e capturar o que vem depois do @

def limpa_descricao(descricao):
    descricao=re.sub(r"\n", " ", descricao) #substituir enter por espaço
    descricao=descricao.strip() #remover espaços em branco no início e no fim da descrição
    return descricao 

conceitos_dict={}

for c in conceitos_designacao[1:]:
    elems=re.split(r'\n',c, maxsplit=1) #dividir o conceito em designação e descrição, maxsplit=1 para dividir apenas na primeira ocorrência do enter
    if len(elems)>1:
        designacao=elems[0]
        #print('designação:' , designacao)
        descricao=elems[1]
        #print('descrição:' , descricao)
        #print("-"*20)
        conceitos_dict[designacao]=descricao
    
    else:
        #Fixe me
        continue

print(len(conceitos_dict))

import json 
def gravar_json(filename, conceitos_dict):

    f_out = open(filename,'w', encoding='utf8')
    json.dump(conceitos_dict,f_out, indent=4, ensure_ascii=False) # o ident é para nao ficar tudo numa linha, e o ensure é para os acentos ficarem direito
    
#json.load() #ler o ficheiro
#json.dump() #escrever no ficheiro

def gera_html(filename, conceitos_dict):
    html = """
<html>
    <head>
    <title>Dicionário Médico</title>
    </head>
    <body>"""

    
    for c in conceitos_dict:
        html += f"""
        <div>
            <p> <b> {c} </b> </p>
            <p> {conceitos_dict[c]} </p>
        
        </div>
        <hr>
        """

    
    html=html+"""</body>
</html>"""  
    f_out = open(filename,'w', encoding='utf8')
    f_out.write(html) 

gera_html("dicionario_medico.html", conceitos_dict)     