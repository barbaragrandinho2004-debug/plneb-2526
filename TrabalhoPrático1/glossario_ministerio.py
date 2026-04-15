import re
import json

def extrair_ministerio_saude(caminho_xml):
    """
    Extrai conceitos médicos, áreas temáticas (categorias) e definições a partir
    de um documento PDF convertido em formato XML. Utiliza técnicas de 
    Rule-based Parsing para limpeza de ruído tipográfico e extração de entidades.
    
    Parâmetros:
        caminho_xml (str): Caminho para o arquivo XML de origem.
        
    Retorna:
        dict: Dicionário estruturado com a terminologia médica.
    """
    print(f"[{caminho_xml}] A iniciar extraçãO ...")
    
    with open(caminho_xml, 'r', encoding='utf-8') as f:
        texto = f.read()

    # ==========================================
    # 1. Pré-Processamento: limpeza tipográfica no xml
    # ==========================================

    # Remove tags estruturais irrelavantes (páginas, metadados do conversor e imagens)
    texto = re.sub(r"</?page.*?>", r"", texto) 
    texto = re.sub(r"</?pdf2xml.*?>", r"", texto)
    texto = re.sub(r"</?image.*?>", r"", texto) 

    # Remoção de estruturas visuais baseada no tamanho da fonte (font size).
    # Elimina números de página no rodapé (15) e siglas de navegação lateral (22, 23, 25),
    # impedindo a sua concatenação indevida com o corpo do texto.
    padrao_fontes_lixo = r'<text[^>]*font="(22|15|25|23)"[^>]*>.*?</text>\n?'
    texto = re.sub(padrao_fontes_lixo, r"", texto)
    
    # 2. Normalização textual 
    # Resolução de ligaturas tipográficas geradas pelo conversor PDF
    texto = re.sub(r'ﬁ', 'fi', texto)
    texto = re.sub(r'ﬂ', 'fl', texto)
    texto = re.sub(r'fi\s+([a-zÀ-ÿ])', r'fi\1', texto) 

    # Padronização de espaçamentos (remoção de quebras de linha estritas)
    texto = re.sub(r'\n', ' ', texto)
    texto = re.sub(r'\s+', ' ', texto)

    # ==========================================
    # 3. Ancoragem e segmentação de entidades
    # ==========================================
    
    # Correção de quebras artificiais em termos a negrito
    texto = re.sub(r'</b></text>\s*<text[^>]*>\s*<b>', ' ', texto)
    # Inserção de marcadores estruturais baseados no padrão visual do documento
    # (Fonte 21 a negrito, ou negrito imediatamente seguido de "Categoria" ou "Ver")
    texto = re.sub(r'<text[^>]*font="21"[^>]*><b>(.*?)</b></text>', r'###TERMO###\1', texto)
    texto = re.sub(r'<b>(.*?)</b></text>\s*<text[^>]*>\s*(?:Categoria|Ver)', r'###TERMO###\1 <text>Categoria', texto)
    
    # Eliminar do documento as restantes tags XML, convertendo-o em texto simples
    texto = re.sub(r'<text[^>]*>|</text>|<i>|</i>|<b>|</b>|<fontspec[^>]*>', ' ', texto)
    texto = re.sub(r'\s+', ' ', texto).strip()

    # Reconstrução de vocábulos fragmentados por hifenização de quebra de linha
    texto = re.sub(r'([a-zA-ZÀ-ÿ])- ([a-zA-ZÀ-ÿ])', r'\1\2', texto)

    # Isolamento do corpo de dados: Descartar o índice e introdução
    partes_inicio = re.split(r'###TERMO###Abordagem médica', texto, maxsplit=1)
    if len(partes_inicio) > 1:
        texto = "###TERMO###Abordagem médica" + partes_inicio[1]

    # Segmentação do texto contínuo numa lista de instâncias independentes
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

    # ==========================================
    # 4. Extração Iterativa de atributos
    # ==========================================

    for bloco in blocos[1:]:

        bloco = bloco.strip()
        if len(bloco) < 3: continue

        # 4.1 Tratamento de Referências Cruzadas (Cross-references)
        match_ver = re.search(r'\s+Ver\s+', bloco, re.IGNORECASE)

        if match_ver:
            partes = re.split(re.escape(match_ver.group(0)), bloco, maxsplit=1)
            termo = re.sub(r'Categoria\s*:?', '', partes[0]).strip()
            if len(termo) > 100: continue # Filtro de ruído

            dicionario_final[termo] = {

                "categoria": ["Referência Cruzada"],
                "descricao": "Ver " + partes[1].strip()
            }

            continue

        # 4.2 Extração de Conceitos Regulares

        pos_cat = bloco.lower().find("categoria")

        if pos_cat != -1:
            termo = bloco[:pos_cat].strip()

            # Filtro dimensional para mitigar a captura de índices residuais
            if len(termo) > 100:
                continue

            resto = bloco[pos_cat:].strip()

            # Limpeza do descritor semântico "Categoria:"
            resto = re.sub(r'^categoria\s*:?\s*', '', resto, flags=re.IGNORECASE)

            # Correções ortográficas inerentes a erros de OCR/Tipografia do PDF
            resto = resto.replace("Demografi a", "Demografia")
            resto = resto.replace("Economia da Saúde", "Economia de Saúde")
            resto = resto.replace("Ciências Sociais e Saúde", "Ciências Sociais em Saúde")

            # Identificação e extração da área temática
            cats_encontradas = []

            for cat in categorias_oficiais:

                if resto.lower().startswith(cat.lower()):
                    cats_encontradas.append(cat)
                    resto = resto[len(cat):].strip()
                    break
                    
            # O que sobra é a descrição
            descricao = resto.strip()

            # Remoção de ruído de rodapé persistente anexado ao final das descrições
            descricao = re.sub(r'\s+[A-Z][a-zÀ-ÿ]+[\w\sÀ-ÿ\-]+\s\d{2,3}$', '', descricao)

            # Validação e estruturação da instância válida
            if termo and len(termo) > 1:

                dicionario_final[termo] = {
                    "categoria": cats_encontradas,
                    "descricao": descricao
                }

    
    # ==========================================
    # 5. Pós-Processamento e recuperação de oclusões
    # ==========================================

    # Algoritmo desenhado para recuperar títulos e categorias que, devido à
    # ausência de formatação a negrito no PDF, ficaram embutidos na definição do termo anterior.
    termos_a_adicionar = {}

    for termo, info in dicionario_final.items():
        descricao = info["descricao"]

        # Expressão regular para detetar: [Início de Frase] + "Categoria:" + [Continuação]
        match = re.search(r'([A-Z][A-Za-zÀ-ÿ\s]+)\s+Categoria\s*:\s*([A-Za-zÀ-ÿ\s,]+)\s+([A-Z].*)', descricao)
        if match:
            novo_termo = match.group(1).strip()
            # Remoção de lixo de cabeçalho anexado ao novo termo
            novo_termo = re.sub(r'^[A-Z]{3,}\s+', '', novo_termo).strip()
            nova_cat = match.group(2).strip()
            nova_def = match.group(3).strip()

            # Truncamento da definição original no ponto exato da oclusão
            texto_antes = descricao[:match.start()].strip()
            texto_antes = re.sub(r'\s+[A-Z]{3,}$', '', texto_antes).strip()
            dicionario_final[termo]["descricao"] = texto_antes

            # Preparação da nova instância resgatada
            termos_a_adicionar[novo_termo] = {
                "categoria": [nova_cat] if nova_cat in categorias_oficiais else [],
                "descricao": nova_def
            }

           

    # Adiciona os termos ao dicionário principal
    dicionario_final.update(termos_a_adicionar)


    # ==========================================
    # 7. Exportação do json
    # ==========================================
    
    f_out = open("jsons_temporarios/ministerio_saude_temp.json", "w", encoding="utf-8")
    json.dump(dicionario_final, f_out, indent=4, ensure_ascii=False)
    f_out.close()

    print(f"Concluído! Extraídos {len(dicionario_final)} conceitos.")
    return dicionario_final

extrair_ministerio_saude("dados/glossario_ministerio_saude.xml")