from bs4 import BeautifulSoup
import requests
import json
import string

url = f"https://www.atlasdasaude.pt/doencasAaZ/"

abcedario = string.ascii_lowercase
res = {}

def extrair_pagina(url):
    html = requests.get(url).text
    soup = BeautifulSoup(html, "html.parser")

    div_doencas = soup.find_all("div", class_="views-row")

    res = {}
    for div in div_doencas:
        designacao = div.div.h3.a.text 
        
        small_descricao = div.find("div", class_="views-field views-field-body").div.text 

        url_full_descricao = div.find("div", class_="views-field views-field-title").a["href"]

        html = requests.get("https://www.atlasdasaude.pt/"+url_full_descricao).text
        soup = BeautifulSoup(html, "html.parser")

        full_descricao = soup.find("div", class_="field field-name-body field-type-text-with-summary field-label-hidden").div.div.text

        res[designacao] = {"small_descs": small_descricao.strip(),
                           "full_desc": full_descricao.strip()}
    return res

for letra in abcedario:
    res = res | extrair_pagina(url+letra) 

f_out = open("doencasTPC.json", "w", encoding="utf8")
json.dump(res, f_out, indent=4, ensure_ascii=False)
f_out.close()