import re
import json
f=open("livrinho.txt", encoding="utf-8")
texto=f.read()

f_conceitos=open("conceitos.json", encoding="utf-8")
conceitos=json.load(f_conceitos) #usamos load porque o ficheiro é um json, se fosse txt usariamos read

black_list=["de", "e", "os"]
def substituir_conceito(match):
    palavra=match[0] #match é um objeto do tipo re.Match, e o [0] é a palavra que foi encontrada
    if palavra in conceitos and palavra not in black_list:
        return f"<a href='' title='{conceitos[palavra]}'>{palavra}</a>" #se a palavra estiver nos conceitos, retorna a palavra com um link para a descrição
    else:
        return palavra

###encontrar conceitos

texto=re.sub(r"\w+", substituir_conceito, texto) 

###gerar html

texto=re.sub(r"\n", "<br>", texto) #substituir as quebras de linha por <br> para que o html fique formatado
texto=re.sub(r"\f", "<hr>", texto) #substituir as quebras de página por <hr> para que o html fique formatado
f_html=open("livro.html", "w", encoding="utf-8")
html_header="""
<html> 
    <head>
        <title> Livro de doenças do aparelho digestivo </title>
        <meta charset="UTF-8">
    </head>

"""

html_body=f"<body> {texto} </body>"
html_footer="</html>"

f_html=open("livro.html", "w", encoding="utf-8")
f_html.write(html_header + html_body + html_footer )
     