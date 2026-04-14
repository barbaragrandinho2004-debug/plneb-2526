import re
import json

def extrair_ministerio_saude(caminho_xml):
    print(f"[{caminho_xml}] A iniciar extraçãO ...")
    
    with open(caminho_xml, 'r', encoding='utf-8') as f:
        texto = f.read()

    
    # 1. LIMPEZA DIRETO NO XML
    
    # Remove as tags de páginas, imagens e pdf2xml que não interessam
    texto = re.sub(r"</?page.*?>", r"", texto) 
    texto = re.sub(r"</?pdf2xml.*?>", r"", texto)
    texto = re.sub(r"</?image.*?>", r"", texto) 

    # Remove números de página (15), siglas laterais (23, 25) e letras capitulares (22)
    padrao_fontes_lixo = r'<text[^>]*font="(22|15|25|23)"[^>]*>.*?</text>\n?'
    texto = re.sub(padrao_fontes_lixo, r"", texto)
    
    

    
    # 2. LIMPEZA INICIAL 
    
    texto = re.sub(r'ﬁ', 'fi', texto)
    texto = re.sub(r'ﬂ', 'fl', texto)
    texto = re.sub(r'fi\s+([a-zÀ-ÿ])', r'fi\1', texto) 

    # Transformar quebras de linha em espaços
    texto = re.sub(r'\n', ' ', texto)
    texto = re.sub(r'\s+', ' ', texto)

    
    # 3. MARCAÇÃO DE TERMOS E LIMPEZA XML
    
    texto = re.sub(r'</b></text>\s*<text[^>]*>\s*<b>', ' ', texto)
    texto = re.sub(r'<text[^>]*font="21"[^>]*><b>(.*?)</b></text>', r'###TERMO###\1', texto)
    texto = re.sub(r'<b>(.*?)</b></text>\s*<text[^>]*>\s*(?:Categoria|Ver)', r'###TERMO###\1 <text>Categoria', texto)
    
    # Limpar o resto do XML
    texto = re.sub(r'<text[^>]*>|</text>|<i>|</i>|<b>|</b>|<fontspec[^>]*>', ' ', texto)
    texto = re.sub(r'\s+', ' ', texto).strip()

    # Correção de Hifenização
    texto = re.sub(r'([a-zA-ZÀ-ÿ])- ([a-zA-ZÀ-ÿ])', r'\1\2', texto)

    # 4. Cortar a parte inicial
    partes_inicio = re.split(r'###TERMO###Abordagem médica', texto, maxsplit=1)
    if len(partes_inicio) > 1:
        texto = "###TERMO###Abordagem médica" + partes_inicio[1]


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

        "Saúde animal", "Vigilância em Saúde", "Recursos humanos em saúde Pública", 

    ]



    # 7. Ciclo 

    for bloco in blocos[1:]:

        bloco = bloco.strip()

        if len(bloco) < 3: continue


        # 2. Identificar se é "Ver" (Referências Cruzadas)

        match_ver = re.search(r'\s+Ver\s+', bloco, re.IGNORECASE)

        if match_ver:

            partes = re.split(re.escape(match_ver.group(0)), bloco, maxsplit=1)

            termo = re.sub(r'Categoria\s*:?', '', partes[0]).strip()

            if len(termo) > 100: continue # Bloqueio de lixo

            

            dicionario_final[termo] = {

                "categoria_area": ["Referência Cruzada"],

                "definicao": "Ver " + partes[1].strip(),

                "fonte": "Ministério da Saúde"

            }

            continue



        # 3. Conceitos Normais (com Categoria)

        pos_cat = bloco.lower().find("categoria")

        if pos_cat != -1:

            termo = bloco[:pos_cat].strip()



            # ==========================================================

            # FILTRO DE TAMANHO

            # Se o termo tiver mais de 100 caracteres, é lixo/índice, por isso saltamos.

            if len(termo) > 100:

                continue

            # ==========================================================
           

            resto = bloco[pos_cat:].strip()

            # Limpa a palavra "Categoria" e os dois pontos

            resto = re.sub(r'^categoria\s*:?\s*', '', resto, flags=re.IGNORECASE)

           # Correções ortográficas das categorias do PDF
            resto = resto.replace("Demografi a", "Demografia")
            resto = resto.replace("Economia da Saúde", "Economia de Saúde")
            resto = resto.replace("Ciências Sociais e Saúde", "Ciências Sociais em Saúde")

            # Extrair categorias oficiais do início do "resto"

            cats_encontradas = []

            for cat in categorias_oficiais:

                if resto.lower().startswith(cat.lower()):

                    cats_encontradas.append(cat)

                    resto = resto[len(cat):].strip()

           

            # O que sobra é a definição

            definicao = resto.strip()

           

            

            # 2. Remove rodapés perdidos no fim da definição (Ex: "Alcoólatra Amamentação exclusiva 19")

            definicao = re.sub(r'\s+[A-Z][a-zÀ-ÿ]+[\w\sÀ-ÿ\-]+\s\d{2,3}$', '', definicao)

           

            
           

            if termo and len(termo) > 1:

                dicionario_final[termo] = {

                    "categoria_area": cats_encontradas,

                    "definicao": definicao,

                    "fonte": "Ministério da Saúde"

                }

    # =========================================================================

    # 8. O "DESENTALADOR" DE TERMOS (Lógica geral e dinâmica)

    # Procura definições que "engoliram" outros termos devido a erros do PDF

    # Padrão: "...texto da def... Nome do Novo Termo Categoria: Categoria da def..."

    # =========================================================================

   

    termos_a_adicionar = {}

   

    for termo, info in dicionario_final.items():

        definicao = info["definicao"]

       

        # Procura a palavra "Categoria:" no meio da definição

        match = re.search(r'([A-Z][A-Za-zÀ-ÿ\s]+)\s+Categoria\s*:\s*([A-Za-zÀ-ÿ\s,]+)\s+([A-Z].*)', definicao)

       

        if match:

            # Encontrou um termo preso!

            novo_termo = match.group(1).strip()

            # Limpar lixo de cabeçalho (ex: "ACI Acidentes...")

            novo_termo = re.sub(r'^[A-Z]{3,}\s+', '', novo_termo).strip()

           

            nova_cat = match.group(2).strip()

            nova_def = match.group(3).strip()

           

            # 1. Limpa a definição do termo original (corta antes do novo termo)

            texto_antes = definicao[:match.start()].strip()

            # Limpa lixo de cabeçalho se houver

            texto_antes = re.sub(r'\s+[A-Z]{3,}$', '', texto_antes).strip()

            dicionario_final[termo]["definicao"] = texto_antes

           

            # 2. Guarda o novo termo para adicionar ao dicionário a seguir

            termos_a_adicionar[novo_termo] = {

                "categoria_area": [nova_cat] if nova_cat in categorias_oficiais else [],

                "definicao": nova_def,

                "fonte": "Ministério da Saúde"

            }

           

    # Junta os termos desentalados ao dicionário principal

    dicionario_final.update(termos_a_adicionar)



    # 8. Gravar JSON

    f_out = open("jsons_temporarios/ministerio_saude_temp.json", "w", encoding="utf-8")

    json.dump(dicionario_final, f_out, indent=4, ensure_ascii=False)

    f_out.close()



    print(f"Concluído! Extraídos {len(dicionario_final)} conceitos.")

    return dicionario_final



extrair_ministerio_saude("dados/glossario_ministerio_saude.xml")