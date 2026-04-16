import re
import json

def extrair_siglas_abreviaturas(caminho_xml):
    print(f"[{caminho_xml}] A extrair Siglas e Abreviaturas ")
    
    with open(caminho_xml, 'r', encoding='utf-8') as f:
        xml_texto = f.read()

    # 1. Isolar a página que tem as abreviaturas e siglas (Página 10)
    match_pagina = re.search(r'<page[^>]*number="10"[^>]*>(.*?)</page>', xml_texto, re.DOTALL)
    
    if not match_pagina:
        print("Erro: Página 10 não encontrada!")
        return
        
    conteudo_pagina = match_pagina.group(1)

    siglas = {}
    abreviaturas = {}

    # 2. Extrair todas as linhas dessa página
    tags = re.findall(r'<text[^>]*>(.*?)</text>', conteudo_pagina)

    for conteudo in tags:
        # Limpar formatações (<b>, <i>, etc)
        linha = re.sub(r'<[^>]+>', '', conteudo).strip()
        
        # Ignorar linhas vazias ou o próprio título da página
        if not linha or "LISTA DE ABREVIATURAS" in linha.upper():
            continue

        # 3. Extração (Chave - Significado)
        match = re.match(r'^([A-Za-zÀ-ÿ0-9\.\s]+?)\s*[-–—]\s*(.+)$', linha)
        
        if match:
            chave = match.group(1).strip()
            significado = match.group(2).strip()

            # 4. Classificação: Abreviatura vs Sigla
            if "." in chave or chave.islower():
                abreviaturas[chave] = significado
            else:
                siglas[chave] = significado

    # 5. Envolver as abreviaturas/siglas na chave principal "Abreviaturas"/"Siglas"
    json_abrev = {
        "Abreviaturas": abreviaturas
    }

    json_siglas = {
        "Siglas": siglas
    }


        

    # 5. EXPORTAÇÃO
    with open("jsons_temporarios/siglas_neologismos.json", "w", encoding="utf-8") as f:
        json.dump(json_siglas, f, indent=4, ensure_ascii=False)

    with open("jsons_temporarios/abreviaturas_neologismos.json", "w", encoding="utf-8") as f:
        json.dump(json_abrev, f, indent=4, ensure_ascii=False)

    print(f"Sucesso! Extraídas {len(siglas)} Siglas e {len(abreviaturas)} Abreviaturas.")
    return siglas, abreviaturas

# Executar
extrair_siglas_abreviaturas("dados/glossario_neologismos_saude.xml")