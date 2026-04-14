import re
import json

def extrair_lista_siglas(caminho_xml):
    print(f"[{caminho_xml}] A iniciar extração cirúrgica da Lista de Siglas...")

    with open(caminho_xml, 'r', encoding='utf-8') as f:
        texto = f.read()

    
    # 1. ISOLAR A SECÇÃO DE SIGLAS 
    
    # as siglas acabam na página 9 por isso cortamos na página 10 para limitar a pesquisa
    partes = re.split(r'<page number="10"', texto, maxsplit=1)
    if len(partes) < 2:
        print("Erro: Não foi possível delimitar a secção de siglas.")
        return
        
    texto_siglas = partes[0]

    
    # 2. LIMPEZA DE RODAPÉS E NÚMEROS DE PÁGINA
    
    texto_siglas = re.sub(r'<text[^>]*>\s*\d+\s*</text>', '', texto_siglas)
    texto_siglas = re.sub(r'<text[^>]*>\s*<b>Siglas</b>\s*</text>', '', texto_siglas, flags=re.IGNORECASE)

    
    # 3. SEPARAR AS SIGLAS
    
    blocos = re.split(r'<text[^>]*font="13"[^>]*><b>(.*?)</b></text>', texto_siglas)

    dicionario_siglas = {}

    for i in range(1, len(blocos) - 1, 2):
        sigla = blocos[i].strip()
        significado_xml = blocos[i+1]

        # 1. Limpar a Sigla
        sigla = re.sub(r'[-–\s]+$', '', sigla).strip()

        # 2. Limpar o Significado (Com correção de ligaturas 'ﬁ')
        significado = significado_xml.replace('ﬁ', 'fi').replace('ﬂ', 'fl')
        significado = re.sub(r'<[^>]+>', ' ', significado)
        significado = re.sub(r'\n', ' ', significado)
        significado = re.sub(r'\s+', ' ', significado).strip()

        # Remove o traço inicial
        significado = re.sub(r'^[-–\s]+', '', significado).strip()

        # Resolve problemas de OCR
        significado = re.sub(r'fi\s+([a-zÀ-ÿ])', r'fi\1', significado)
        significado = re.sub(r'([a-zA-ZÀ-ÿ])- ([a-zA-ZÀ-ÿ])', r'\1\2', significado)

        # 3. Validação Final e Gravação
        if len(sigla) >= 2 and len(significado) > 3:
            dicionario_siglas[sigla] = significado

    
    # 4. ORDENAR E EXPORTAR JSON
    
    # Ordena as siglas alfabeticamente
    dicionario_siglas = dict(sorted(dicionario_siglas.items(), key=lambda item: item[0].lower()))

    with open("jsons_temporarios/ministerio_saude_siglas.json", "w", encoding="utf-8") as f_out:
        json.dump(dicionario_siglas, f_out, indent=4, ensure_ascii=False)

    print(f"Concluído! Foram extraídas {len(dicionario_siglas)} siglas.")
    return dicionario_siglas

# Executa o código
extrair_lista_siglas("dados/glossario_ministerio_saude.xml")