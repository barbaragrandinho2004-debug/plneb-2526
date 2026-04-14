import re
import json

def extrair_neologismos(caminho_xml):
    print(f"[{caminho_xml}] A iniciar extração final com a ordem natural do livro...")
    
    f = open(caminho_xml, 'r', encoding='utf-8')
    texto = f.read()

    # 1. Limpeza de quebras de linha e códigos HTML
    texto = re.sub(r'\n', ' ', texto)
    texto = re.sub(r'\s+', ' ', texto)
    texto = re.sub(r'&#34;', '"', texto) # Transforma aspas HTML em aspas normais

    # =========================================================================
    # 1.5 O MATA-QUEBRAS DE PÁGINA (Para recuperar os 5 termos perdidos)
    # Apagamos as quebras de página e imagens ANTES de procurar a âncora
    texto = re.sub(r'<page[^>]*>|</page>|<image[^>]*>', ' ', texto)
    # Apagamos os cabeçalhos chatos que ficam no meio das páginas 
    texto = re.sub(r'<text[^>]*>\s*([A-Z][a-z]+, [A-Z][a-z]+ \d{4}|\d{2,3})\s*</text>', ' ', texto)
    # =========================================================================

    # 2. Marcação dos termos (Âncora s.m./s.f. - Tolerante a espaços extra do autor)
    texto = re.sub(r'<text[^>]*>\s*([^<]+?)\s*</text>\s*<text[^>]*>\s*<i>\s*(s\.m\.|s\.f\.)\s*</i>\s*</text>', r'###TERMO###\1 @\2@', texto)
    
    # 3. Limpeza total de tags XML
    texto = re.sub(r'<text[^>]*>|</text>|<i>|</i>|<b>|</b>|<image[^>]*>|<page[^>]*>|</page>|<\?xml[^>]*>|<!DOCTYPE[^>]*>|<fontspec[^>]*>', ' ', texto)
    texto = re.sub(r'\s+', ' ', texto).strip()

    # 3.5 União de sílabas hifenizadas
    texto = re.sub(r'([a-z])- ([a-z])', r'\1\2', texto)

    # 3.8 Correções cirúrgicas (Recupera a Distrofia que perdeu a formatação)
    texto = re.sub(r'distrofia muscular progressiva s\.f\. progressive', r'###TERMO###distrofia muscular progressiva @s.f.@ progressive', texto)

    # 4. Corte do lixo inicial
    partes_inicio = re.split(r'###TERMO###abeta', texto, maxsplit=1)
    if len(partes_inicio) > 1:
        texto = "###TERMO###abeta" + partes_inicio[1]

    # 5. Processamento dos blocos
    blocos = re.split(r'###TERMO###', texto)
    dicionario_final = {}

    for bloco in blocos[1:]:
        bloco = bloco.strip()
        if len(bloco) < 3: 
            continue
        
        elems_gramatica = re.split(r'@(s\.m\.|s\.f\.)@', bloco, maxsplit=1)
        
        if len(elems_gramatica) > 2:
            termo = elems_gramatica[0].strip()
            genero = elems_gramatica[1].strip()
            resto = elems_gramatica[2].strip()
            
            # Traduções
            elems_ing = re.split(r'\[ing\];?\s*', resto, maxsplit=1)
            trad_ing = ""
            if len(elems_ing) > 1:
                trad_ing = elems_ing[0].strip()
                resto = elems_ing[1].strip()
                
            elems_esp = re.split(r'\[esp\]\s*|\[es\s', resto, maxsplit=1)
            trad_esp = ""
            if len(elems_esp) > 1:
                trad_esp = elems_esp[0].strip()
                resto = elems_esp[1].strip()
            
            # Citação (Apanha "..." ou "… " ou ".”" ou ".”")
            elems_citacao = re.split(r'\s*[“"”]\s*[\.…]+|\s*[\.…]+\s*[“"”]', resto, maxsplit=1)
            definicao_completa = elems_citacao[0].strip()
            
            # Limpeza final de páginas
            definicao_completa = re.sub(r'\s*\(\d+.*?\)*$', '', definicao_completa)
            definicao_completa = re.sub(r'\s\d{2,3}$', '', definicao_completa)

            # =========================================================================
            # NOVO: EXTRAIR A SIGLA PARA UM CAMPO PRÓPRIO
            sigla = ""
            # Procura se a definição começa por "Sigla: [LETRAS] "
            match_sigla = re.match(r'^Sigla:\s*([A-Z0-9\-]+)\s+(.*)', definicao_completa)
            if match_sigla:
                sigla = match_sigla.group(1) # Guarda a sigla (ex: AVCI)
                definicao_completa = match_sigla.group(2) # Guarda o resto da definição limpa
            # =========================================================================

            # CORREÇÃO NA HORA: Consertamos o "transtorno"
            if termo == "transtorno cognitivo":
                termo = "transtorno cognitivo leve"
                genero = "s.m."
                definicao_completa = definicao_completa.replace("leve Distúrbio", "Distúrbio").strip()

            if termo and termo[0].islower():
                dicionario_final[termo] = {
                    "classe_gramatical": genero,
                    "sigla": sigla,                  
                    "traducao_en": trad_ing,
                    "traducao_es": trad_esp,
                    "definicao": definicao_completa,
                    "fonte": "Glossário de Neologismos"
                }

    # 6. Gravar o JSON
    f_out = open("jsons_temporarios/neologismos_temp.json", "w", encoding="utf-8")
    json.dump(dicionario_final, f_out, indent=4, ensure_ascii=False)
    f_out.close()

    print(f"Sucesso! Extraídos {len(dicionario_final)} neologismos com a ordem corrigida.")
    return dicionario_final

extrair_neologismos("dados/glossario_neologismos_saude.xml")