import re
import json

def extrair_ministerio_saude(caminho_xml):
    """
    Parser especializado para o Glossário do Ministério da Saúde.
    Devolve um dicionário estruturado.
    """
    print(f"[{caminho_xml}] A iniciar extração do Ministério da Saúde...")
    
    with open(caminho_xml, "r", encoding="utf-8") as f:
        texto = f.read()

    # 1. Limpeza de Metadados XML
    texto = re.sub(r'<\?xml.*?\?>', '', texto)
    texto = re.sub(r'<!DOCTYPE.*?>', '', texto)
    texto = re.sub(r'<fontspec.*?>', '', texto)
    texto = re.sub(r'<image.*?>', '', texto)
    texto = re.sub(r'<page.*?>', '', texto)
    texto = re.sub(r'</page>', '', texto)

    # 2. Remoção de Ruído Específico (Números de página e cabeçalhos de letras)
    texto = re.sub(r'<text[^>]*font="(12|15)"[^>]*>\d+</text>', '', texto)
    texto = re.sub(r'<text[^>]*font="22"[^>]*>.*?</text>', '', texto)

    # 3. Marcação de Termos (Âncoras)
    texto = re.sub(r'<text[^>]*font="21"[^>]*><b>(.*?)</b></text>', r'###TERMO###\1', texto)

    # 4. Limpeza de tags de texto restantes
    texto = re.sub(r'<text[^>]*>', '', texto)
    texto = re.sub(r'</text>', ' ', texto)
    texto = re.sub(r'<i>', '', texto)
    texto = re.sub(r'</i>', '', texto)
    texto = re.sub(r'<b>', '', texto)
    texto = re.sub(r'</b>', '', texto)

    # Juntar linhas e remover espaços excessivos
    texto = texto.replace('\n', ' ')
    texto = re.sub(r'\s+', ' ', texto)

    # 5. Extração por blocos
    blocos = texto.split('###TERMO###')
    dicionario_final = {}

    # Lista oficial de categorias para deteção exata
    categorias_oficiais = [
        "Administração e Planejamento em Saúde", "Acidentes e Violência",
        "Alimentação e Nutrição", "Ambiente e Saúde", "Atenção à Saúde",
        "Ciência e Tecnologia em Saúde", "Ciências Sociais em Saúde",
        "Comunicação em Saúde", "Demograﬁ a", "Direito Sanitário",
        "Doenças", "Drogas de uso terapêutico e social", "Drogas de Uso Terapêutico e Social",
        "Economia de saúde", "Economia de Saúde", "Epidemiologia",
        "Eqüidade em saúde e social", "Ética e bioética",
        "História da saúde pública", "Medicamentos, vacinas e insumos",
        "Medicamentos, Vacinas e Insumos", "Políticas públicas e saúde",
        "Políticas Públicas e Saúde", "Promoção e Educação em Saúde",
        "Saúde animal", "Vigilância em Saúde", "Recursos humanos em saúde"
    ]

    for bloco in blocos:
        bloco = bloco.strip()
        if not bloco or len(bloco) < 3 or '<pdf2xml' in bloco:
            continue
        
        # 1. Identificar se é uma Referência Cruzada ("Ver ...")
        if " Ver " in bloco:
            partes = bloco.split(" Ver ", 1)
            termo = partes[0].strip()
            dicionario_final[termo] = {
                "categoria_area": ["Referência Cruzada"],
                "definicao": "Ver " + partes[1].strip(),
                "fonte": "Ministério da Saúde"
            }
            continue

        # 2. Tentar extrair Categorias e Definição
        termo = ""
        categorias_encontradas = []
        resto_texto = bloco

        # O termo vem sempre antes da primeira categoria
        # Vamos procurar qual categoria oficial aparece primeiro no bloco
        primeira_pos = len(bloco)
        for cat in categorias_oficiais:
            pos = bloco.find(cat)
            if pos != -1 and pos < primeira_pos:
                primeira_pos = pos
        
        termo = bloco[:primeira_pos].strip()
        termo = termo.replace("Categoria:", "").strip()

        resto_texto = bloco[primeira_pos:].strip()

        # Extrair todas as categorias que aparecem no início do resto_texto
        ainda_tem_categorias = True
        while ainda_tem_categorias:
            ainda_tem_categorias = False
            for cat in categorias_oficiais:
                if resto_texto.startswith(cat):
                    categorias_encontradas.append(cat)
                    resto_texto = resto_texto[len(cat):].strip()
                    ainda_tem_categorias = True
                    break
        
        # Remover o prefixo "Categoria:" se ele tiver ficado no início da definição
        definicao = resto_texto.lstrip("Categoria:").strip()

        # Limpeza final da definição (remover marcas de página como ACI, AUT, etc)
        # Estas marcas têm sempre 3 letras maiúsculas no fim da linha
        definicao = re.sub(r'\s[A-Z]{3}$', '', resto_texto)

        if termo and (categorias_encontradas or definicao):
            dicionario_final[termo] = {
                "categoria_area": categorias_encontradas,
                "definicao": definicao,
                "fonte": "Ministério da Saúde"
            }

    # Limpeza de fragmentos (remover chaves que não começam por Letra)
    dicionario_final = {k: v for k, v in dicionario_final.items() if k[0].isalpha()}

    print(f"[{caminho_xml}] Extraídos {len(dicionario_final)} conceitos.")
    return dicionario_final

