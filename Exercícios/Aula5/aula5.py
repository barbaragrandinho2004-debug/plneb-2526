from bs4 import BeautifulSoup
import requests
import json
import string

url = f"https://www.atlasdasaude.pt/doencasAaZ/"

#abcedario = soup.find_all("div", class_="views-summary views-summary-unformatted").a("href")
#abcedario = "abcdefghijklmnopqrstuvwxyz"
abcedario = string.ascii_lowercase
res = {}

def extrair_pagina(url):
    html = requests.get(url).text
    soup = BeautifulSoup(html, "html.parser")

    div_doencas = soup.find_all("div", class_="views-row")

    res = {}
    for div in div_doencas:
        designacao = div.div.h3.a.text #no div entra no primeiro div que entra no h3 que entra no a e vai buscar so o texto
        descricao = div.find("div", class_="views-field views-field-body").div.text #o .text vai devolver o texto de todos os filhos a partir do ponto que estamos, por isso convem ser o mais especifico possivel
        res[designacao] = descricao.strip()
    return res

for letra in abcedario:
    res = res | extrair_pagina(url+letra) #juntar dicionario

f_out = open("doencas.json", "w", encoding="utf8")
json.dump(res, f_out, indent=4, ensure_ascii=False)
f_out.close()


#<div class="views-row views-row-30 views-row-even views-row-last">
#   <div class="views-field views-field-title">        
#       <h3 class="field-content">
#           <a href="/content/ataque-epileptico">Ataque epiléptico</a>
#       </h3>  
#   </div>  
#   <div class="views-field views-field-body">        
#       <div class="field-content"> 
#           <p>Os sintomas da epilepsia, ou dito correctamente, de uma crise epiléptica, são definidos pelos doentes como singulares impressões sensoriais. Na prática o doente exibe sintomas convulsivos, contracções musculares involuntárias e desmaios.</p>
#       </div>  
#   </div>  
#</div>
  