import re
import json

def extrair_termos_populares(caminho_xml):

    """
    Processa o ficheiro XML e devolve um dicionário com os conceitos extraídos,
    pronto a ser importado e utilizado pelo main.py.
    """
    print(f"[{caminho_xml}] A iniciar extração de Termos Populares...")

    with open(caminho_xml, "r", encoding="utf-8") as f:
        texto = f.read()

    # ==========================================
    # FASE 1: LIMPEZA BÁSICA 
    # ==========================================
    texto = re.sub(r'<\?xml.*?\?>', '', texto)
    texto = re.sub(r'<!DOCTYPE.*?>', '', texto)
    texto = re.sub(r'<fontspec.*?>', '', texto)
    texto = re.sub(r'<page.*?>', '', texto)
    texto = re.sub(r'</page>', '', texto)
    texto = re.sub(r'<text[^>]*>', '', texto)
    texto = re.sub(r'</text>', '', texto)
    texto = re.sub(r'<i>', '', texto)
    texto = re.sub(r'</i>', '', texto)

    # Converter quebras de linha em espaços para a Regex deslizar bem
    texto = texto.replace('\n', ' ')
    texto = re.sub(r'\s+', ' ', texto)

    # ==========================================
    # FASE 2: EXTRAÇÃO BLINDADA COM REGEX
    # ==========================================
    
    # Esta Regex usa um "lookahead" negativo (?!...) 
    # Garante que a definição NUNCA atravessa a fronteira de outro <b> ou (pop)

    regex = r'<b>([^<]+)</b>\s*,\s*((?:(?!<b>|\(pop\)).)+)\s*\(pop\)|((?:(?!<b>|\(pop\)).)+)\s*\(pop\)\s*,\s*<b>([^<]+)</b>'
    
    encontros = re.findall(regex, texto)
    dicionario_termos = {}

    for match in encontros:
        # Se for o Padrão A (Termo Técnico primeiro)
        if match[0]: 
            tecnico = match[0].strip()
            popular = match[1].strip()
        # Se for o Padrão B (Definição Popular primeiro)
        else:
            popular = match[2].strip()
            tecnico = match[3].strip()

        # Limpeza cirúrgica de pequenos lixos e vírgulas iniciais
        tecnico = tecnico.replace('/b>', '').replace('<b>', '').strip()
        popular = popular.replace('/b>', '').replace('<b>', '').lstrip(', ').strip()

        # Remover letras de capítulos soltas (ex: b>A< )
        tecnico = re.sub(r'b>[A-Z]< ', '', tecnico)
        popular = re.sub(r'b>[A-Z]< ', '', popular)

        # Adicionar ao Dicionário 
        if tecnico and popular and len(tecnico) > 1:
            if tecnico not in dicionario_termos:
                dicionario_termos[tecnico] = {
                    "categoria_area": ["Termos Populares"],
                    "termos_populares": []
                }
            
            # Adicionar a definição se ainda não existir
            if popular not in dicionario_termos[tecnico]["termos_populares"]:
                dicionario_termos[tecnico]["termos_populares"].append(popular)

    # ==========================================
    # FASE 3: RETURN PARA O MAIN.PY
    # ==========================================
    print(f"[{caminho_xml}] Extraídos {len(dicionario_termos)} conceitos.")
    
    # Em vez de guardar em JSON, devolvemos a variável diretamente!
    return dicionario_termos