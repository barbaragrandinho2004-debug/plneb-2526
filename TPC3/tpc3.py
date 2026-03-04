import re
import json

# 1. Ler ficheiro txt original
f = open("dicionario_medico.txt", "r", encoding="utf-8")
texto = f.read()
f.close()


# Substituir as quebras de página (form feed) por quebras de linha normais
texto = re.sub(r"\f", "\n", texto)

# Marcar temporariamente os conceitos 
texto = re.sub(r"\n\n", "\n\n@", texto)

# Corrigir quebras a meio de descrições (juntar frases cortadas pelo \f)
texto = re.sub(r"([a-zà-úç])\s*\n\n@\n\s*([a-zà-úç])", r"\1 \2", texto)

# Corrigir quebras logo após o final de uma definição
texto = re.sub(r"\n\n@\n([A-ZÀ-ÚÇ])", r"\n\1", texto)

# Limpar a nossa marcação (@) para que o texto fique bonito
texto = re.sub(r"@", "", texto)

# Gravar o texto tratado para provar que a limpeza funcionou
f_tratado = open("dicionario_medico_tratado.txt", "w", encoding="utf-8")
f_tratado.write(texto)
f_tratado.close()


# Como limpámos os @, agora separamos usando apenas os duplos enters válidos que sobraram
conceitos_designacao = re.split(r"\n\n", texto)
print(f"Foram encontrados {len(conceitos_designacao) - 1} possíveis conceitos.")

def limpa_descricao(descricao):
    descricao = re.sub(r"\n", " ", descricao) # substituir enter por espaço
    descricao = descricao.strip() # remover espaços em branco no início e no fim
    return descricao 

conceitos_dict = {}

for c in conceitos_designacao[1:]:
    # maxsplit=1 garante que a descrição não é cortada se tiver enters pelo meio
    elems = re.split(r'\n', c, maxsplit=1) 
    if len(elems) > 1:
        designacao = elems[0].strip()
        descricao = limpa_descricao(elems[1])
        conceitos_dict[designacao] = descricao
    else:
        continue

print(f"Total de conceitos guardados no dicionário: {len(conceitos_dict)}")


def gravar_json(filename, dict_conceitos):
    f_out = open(filename, 'w', encoding='utf-8')
    json.dump(dict_conceitos, f_out, indent=4, ensure_ascii=False) 
    f_out.close()

def gera_html(filename, dict_conceitos):
    html = """
<html>
    <head>
    <title>Dicionário Médico</title>
    <meta charset="utf-8">
    </head>
    <body>"""
    
    for c in dict_conceitos:
        html += f"""
        <div>
            <p> <b> {c} </b> </p>
            <p> {dict_conceitos[c]} </p>
        </div>
        <hr>
        """
    
    html += """</body>\n</html>"""  
    
    f_out = open(filename, 'w', encoding='utf-8')
    f_out.write(html)
    f_out.close()

# Executar a criação dos ficheiros
gravar_json("dicionario_medico.json", conceitos_dict)
gera_html("dicionario_medico.html", conceitos_dict)