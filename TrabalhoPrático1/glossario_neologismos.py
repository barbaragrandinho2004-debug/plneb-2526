import re
import json

def extrair_neologismos(caminho_xml):
    """
    Extrai neologismos, traduções e definições de um arquivo XML gerado a partir de um PDF, estruturando 
    os dados resultantes num dicionário JSON.
    
    Parâmetros:
        caminho_xml (str): Caminho para o arquivo XML de origem.
        
    Retorna:
        dict: Dicionário contendo os neologismos estruturados.
    """
    print(f"[{caminho_xml}] A iniciar extração...")
    
    f = open(caminho_xml, 'r', encoding='utf-8')
    texto = f.read()

    # ==========================================
    # 1. Normalização Inicial do Texto
    # ==========================================

    # Substitui quebras de linha e múltiplos espaços por um único espaço
    texto = re.sub(r'\n', ' ', texto)
    texto = re.sub(r'\s+', ' ', texto)
    texto = re.sub(r'&#34;', '"', texto) # Transforma aspas HTML em aspas normais

    # 2. Remoção de Elementos Estruturais e Cabeçalhos
    # Remove delimitadores de página e de imagens
    texto = re.sub(r'<page[^>]*>|</page>|<image[^>]*>', ' ', texto)
    # Remove cabeçalhos que contêm o mês, ano e números de página
    texto = re.sub(r'<text[^>]*>\s*([A-Z][a-z]+, [A-Z][a-z]+ \d{4}|\d{2,3})\s*</text>', ' ', texto)
    
    # ==========================================
    # 3. Identificação e Marcação dos Termos Principais
    # ==========================================

    # Utiliza a tag <i> contendo a classe gramatical (s.m. ou s.f.) como âncora
    # para isolar o neologismo e a sua respectiva classe.
    texto = re.sub(r'<text[^>]*>\s*([^<]+?)\s*</text>\s*<text[^>]*>\s*<i>\s*(s\.m\.|s\.f\.)\s*</i>\s*</text>', r'###TERMO###\1 @\2@', texto)
    
    # 4. Remoção de Tags XML Residuais e Correções Ortográficas
    # Remove tags de itálico e negrito sem inserir espaços, preservando a junção das palavras
    texto = re.sub(r'<i>|</i>|<b>|</b>', '', texto)
    # Remove as restantes tags XML substituindo-as por espaço em branco
    texto = re.sub(r'<text[^>]*>|</text>|<\?xml[^>]*>|<!DOCTYPE[^>]*>|<fontspec[^>]*>', ' ', texto)
    texto = re.sub(r'\s+', ' ', texto).strip()

    # Corrige a hifenização resultante de quebras de linha (ex: pa- lavra -> palavra)
    texto = re.sub(r'([a-z])- ([a-z])', r'\1\2', texto)

    # Tratamento de exceção: Corrige o termo cuja formatação original estava corrompida
    texto = re.sub(r'distrofia muscular progressiva s\.f\. progressive', r'###TERMO###distrofia muscular progressiva @s.f.@ progressive', texto)

    # 5. Isolamento do Corpo do Dicionário
    # Descarta o material introdutório segmentando o texto no primeiro neologismo válido ("abeta")
    partes_inicio = re.split(r'###TERMO###abeta', texto, maxsplit=1)
    if len(partes_inicio) > 1:
        texto = "###TERMO###abeta" + partes_inicio[1]

    # ==========================================
    # 6. Segmentação e Processamento Iterativo dos Neologismos
    # ==========================================

    blocos = re.split(r'###TERMO###', texto)

    dicionario_final = {}
    siglas_embutidas = {}

    for bloco in blocos[1:]:
        bloco = bloco.strip()
        if len(bloco) < 3: 
            continue
        
        # Separa o bloco nas três componentes primárias: [0] Termo, [1] Classe Gramatical, [2] Restante
        elems_gramatica = re.split(r'@(s\.m\.|s\.f\.)@', bloco, maxsplit=1)
        
        if len(elems_gramatica) > 2:
            termo = elems_gramatica[0].strip()
            genero = elems_gramatica[1].strip()
            resto = elems_gramatica[2].strip()
            
            # 6.1. Extração da Tradução para o idioma Inglês
            elems_ing = re.split(r'\[ing\];?\s*', resto, maxsplit=1)
            trad_ing = ""
            if len(elems_ing) > 1:
                trad_ing = elems_ing[0].strip()
                resto = elems_ing[1].strip()

            # 6.2. Extração da Tradução para o idioma Espanhol   
            elems_esp = re.split(r'\[esp\]\s*|\[es\s', resto, maxsplit=1)
            trad_esp = ""
            if len(elems_esp) > 1:
                trad_esp = elems_esp[0].strip()
                resto = elems_esp[1].strip()

            # Tratamento de exceção documental (Tradução embutida na definição por erro do PDF)
            if termo == "encefalopatia espongiforme":
                trad_esp = "encefalopatía espongiforme"
                resto = resto.replace("encefalopatía espongiforme", "").strip()
            
            # 6.3. Extração da Definição (Isolando citações e exemplos práticos)
            # O delimitador baseia-se na presença de aspas seguidas ou precedidas de pontuação
            elems_citacao = re.split(r'\s*[“"”]\s*[\.…]+|\s*[\.…]+\s*[“"”]', resto, maxsplit=1)
            descricao_completa = elems_citacao[0].strip()
            
            # Remoção de numerações de página residuais no final da string
            descricao_completa = re.sub(r'\s*\(\d+.*?\)*$', '', descricao_completa)
            descricao_completa = re.sub(r'\s\d{2,3}$', '', descricao_completa)

            
            # 6.4. Extração de Sigla
            # Captura a sigla apenas se a definição iniciar pelo padrão "Sigla: XYZ"
            sigla = ""
            match_sigla = re.match(r'^Sigla:\s*([A-Z0-9\-]+)\s+(.*)', descricao_completa)
            if match_sigla:
                sigla = match_sigla.group(1)
                descricao_completa = match_sigla.group(2)
            

            # Correção de anomalia morfológica específica do documento
            if termo == "transtorno cognitivo":
                termo = "transtorno cognitivo leve"
                descricao_completa = descricao_completa.replace("leve Distúrbio", "Distúrbio").strip()

            # 7. Estruturação Final e Validação
            # Assegura que o termo é válido e inicia por letra minúscula (padrão tipográfico do glossário)
            if termo and termo[0].islower():
                entrada = {      
                    "descricao": descricao_completa,           
                    "traducoes": {
                        "EN": trad_ing,
                        "ES": trad_esp
                    }
                
                }
                dicionario_final[termo] = entrada

                if sigla:
                    siglas_embutidas[sigla] = termo.capitalize()


    # ==========================================
    # 8. Exportação dos Dados Estruturados
    # ==========================================
    
    with open("jsons_temporarios/neologismos_temp.json", "w", encoding="utf-8") as f_out:
        json.dump(dicionario_final, f_out, indent=4, ensure_ascii=False)

    # Exportar as Siglas 
    siglas_ordenadas = dict(sorted(siglas_embutidas.items(), key=lambda item: item[0].lower()))
    json_siglas_final = {
        "Siglas": siglas_ordenadas
    }
    with open("jsons_temporarios/siglas_embutidas_neologismos.json", "w", encoding="utf-8") as f_out_siglas:
        json.dump(json_siglas_final, f_out_siglas, indent=4, ensure_ascii=False)

    print(f"Concluído! Foram extraídos {len(dicionario_final)} conceitos.")
    print(f"Bónus: {len(siglas_ordenadas)} siglas embutidas foram extraídas para um ficheiro separado!")
    return dicionario_final

extrair_neologismos("dados/glossario_neologismos_saude.xml")