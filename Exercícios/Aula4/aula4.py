import re
import json

f = open("dicionario_medico.xml", encoding="utf-8")

texto = f.read()

texto=re.sub(r"</?text.*?>", "", texto) #substituir tudo o que está entre text por vazio 
texto=re.sub(r"</?page.*?>", "", texto) 
#marcar conceitos

#com split

#texto=re.sub(r"</b>", "", texto) 
#conceitos_designacao=re.split(r"<b>", texto)
#print(len(conceitos_designacao))

conceitos_designacao=re.findall(r"<b>(.*)</b>\n([^<]+)", texto) 
print(conceitos_designacao)

# nota - \s apanha \t, \n, \r, \f, \v - nao foi usada mas é para ter conhecimento de que existe

#podiamos usar o .strip para limpar os espacos em branco no inicio e no fim da string

res={}
for termo, desc in conceitos_designacao:
    res[termo]=desc.strip()

f_out=open("conceitos.json", "w", encoding="utf-8")
json.dump(res, f_out, indent=4, ensure_ascii=False)
f_out.close()