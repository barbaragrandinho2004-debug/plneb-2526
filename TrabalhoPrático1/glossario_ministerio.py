import re
import json

def extrair_ministerio_saude(caminho_xml):
    print(f"[{caminho_xml}] A iniciar extração ...")
    
    # Abertura do ficheiro 
    f = open(caminho_xml, 'r', encoding='utf-8')
    texto = f.read()

    # 1. Limpeza Inicial com re.sub
    texto = re.sub(r'ﬁ', 'fi', texto)
    texto = re.sub(r'ﬂ', 'fl', texto)
    texto = re.sub(r'fi nanceiro', 'financeiro', texto)
    texto = re.sub(r'defi ciência', 'deficiência', texto)
    texto = re.sub(r'\n', ' ', texto)
    texto = re.sub(r'\s+', ' ', texto)
    

    # 2. TRUQUE: Colar os termos partidos
    texto = re.sub(r'</b></text>\s*<text[^>]*font="21"[^>]*><b>', ' ', texto)

    # 3. Marcar termos para extração (ANTES de cortar o texto!)
    texto = re.sub(r'<text[^>]*font="21"[^>]*><b>(.*?)</b></text>', r'###TERMO###\1', texto)

    # 4. Limpeza das tags XML
    texto = re.sub(r'<text[^>]*>|</text>|<i>|</i>|<b>|</b>|<image[^>]*>|<page[^>]*>|</page>|<\?xml[^>]*>|<!DOCTYPE[^>]*>|<fontspec[^>]*>', ' ', texto)
    texto = re.sub(r'\s+', ' ', texto)
    texto = texto.strip()

    # CORREÇÃO DA HIFENIZAÇÃO 
    # Procura uma letra minúscula + hífen + espaço + letra minúscula (ex: "i- b") 
    # e junta tudo ("ib"), transformando "li- berdade" em "liberdade"
    texto = re.sub(r'([a-z])- ([a-z])', r'\1\2', texto)
    
    # Limpar cabeçalhos de página perdidos como o " V 106 "
    texto = re.sub(r' [A-Z] \d{2,3} ', ' ', texto)

    # 5. Cortar lixo inicial (Sumário) usando re.split com maxsplit=1 (Como na aula)
    partes_inicio = re.split(r'###TERMO###Abordagem médica', texto, maxsplit=1)
    if len(partes_inicio) > 1:
        texto = "###TERMO###Abordagem médica" + partes_inicio[1]

    # 6. Dividir os conceitos (Igual ao conceitos2 = re.split(...) da aula)
    blocos = re.split(r'###TERMO###', texto)
    dicionario_final = {}
    
    categorias_oficiais = [
        "Administração e Planejamento em Saúde", "Acidentes e Violência", 
        "Alimentação e Nutrição", "Ambiente e Saúde", "Atenção à Saúde", 
        "Ciência e Tecnologia em Saúde", "Ciências Sociais em Saúde", 
        "Comunicação em Saúde", "Demografia", "Direito Sanitário", 
        "Doenças", "Drogas de uso terapêutico e social", "Drogas de Uso Terapêutico e Social", 
        "Economia de saúde", "Economia de Saúde", "Epidemiologia", 
        "Eqüidade em saúde e social", "Ética e bioética", 
        "História da saúde pública", "Medicamentos, vacinas e insumos", 
        "Medicamentos, Vacinas e Insumos", "Políticas públicas e saúde", 
        "Políticas Públicas e Saúde", "Promoção e Educação em Saúde", 
        "Saúde animal", "Vigilância em Saúde", "Recursos humanos em saúde"
    ]

    # 7. Ciclo For (Começa no [1:] porque o [0] é vazio antes do primeiro termo)
    for bloco in blocos[1:]:
        bloco = bloco.strip()
        if len(bloco) < 3: 
            continue
        
        # Identificar se é "Ver ..."
        if " Ver " in bloco:
            elems = re.split(r" Ver ", bloco, maxsplit=1)
            if len(elems) > 1:
                termo = re.sub(r"Categoria:", "", elems[0]).strip()
                if termo and termo[0].isupper():
                    definicao = "Ver " + elems[1].strip()
                    
                    if termo == "Zalcitabina":
                        definicao = re.split(r"As áreas temáticas", definicao, maxsplit=1)[0].strip()
                        
                    dicionario_final[termo] = {
                        "categoria_area": ["Referência Cruzada"], 
                        "definicao": definicao, 
                        "fonte": "Ministério da Saúde"
                    }
                    if termo == "Zalcitabina":
                        break
            continue

        # Encontrar categoria
        primeira_pos = len(bloco)
        for cat in categorias_oficiais:
            pos = bloco.find(cat)
            if pos != -1 and pos < primeira_pos:
                primeira_pos = pos
        
        termo = bloco[:primeira_pos]
        termo = re.sub(r"Categoria:", "", termo).strip()
        
        # Validação
        if not termo or not termo[0].isupper() or len(termo) < 3:
            continue

        resto_texto = bloco[primeira_pos:].strip()

        # Extrair categorias
        categorias_encontradas = []
        ainda_tem_categorias = True
        while ainda_tem_categorias:
            ainda_tem_categorias = False
            for cat in categorias_oficiais:
                if resto_texto.startswith(cat):
                    categorias_encontradas.append(cat)
                    resto_texto = re.sub(cat, "", resto_texto, count=1).strip()
                    ainda_tem_categorias = True
                    break
        
        # Limpar definição
        definicao = re.sub(r"Categoria:", "", resto_texto).strip()
        definicao = re.sub(r'\s[A-Z]{3}$', '', definicao)

        # Cortar lixo final (Travão de segurança)
        if "As áreas temáticas" in definicao:
            definicao = re.split(r"As áreas temáticas", definicao, maxsplit=1)[0].strip()

        if definicao:
            dicionario_final[termo] = {
                "categoria_area": categorias_encontradas,
                "definicao": definicao,
                "fonte": "Ministério da Saúde"
            }
            if termo == "Zalcitabina":
                break

    # 8. Gravar JSON na pasta temporária
    f_out = open("jsons_temporarios/ministerio_saude_temp.json", "w", encoding="utf-8")
    json.dump(dicionario_final, f_out, indent=4, ensure_ascii=False)
    f_out.close()

    # O teu print querido para saberes quantos tens!
    print(f"Sucesso! Extraídos {len(dicionario_final)} conceitos.")
    return dicionario_final


# Lembra-te de teres a pasta 'jsons_temporarios' já criada no lado esquerdo do VS Code!
extrair_ministerio_saude("dados/glossario_ministerio_saude.xml")