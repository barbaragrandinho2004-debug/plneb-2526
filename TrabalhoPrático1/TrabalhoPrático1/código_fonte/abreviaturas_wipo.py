import re
import json

# 1. Abrir e ler o ficheiro XML completo
caminho_xml = 'dados/wipopearl_covid.xml'

with open(caminho_xml, 'r', encoding='utf-8') as f:
    texto = f.read()

# ==========================================
# CORTAR AS EXTREMIDADES DO DOCUMENTO 
# ==========================================

# Cortar tudo o que está para trás da "List of abbreviations"
start_match = re.search(r'<b>List of abbreviations </b>', texto)
if start_match:
    texto = texto[start_match.end():]

# Cortar tudo o que está para a frente do "Multilingual Glossary"
end_match = re.search(r'<b>Multilingual Glossary </b>', texto)
if end_match:
    texto = texto[:end_match.start()]

# ==========================================
# EXTRAÇÃO E PROCESSAMENTO DOS DADOS
# ==========================================

# Apanhamos tudo o que é font="6" para ignorar os números de página (font="4")
linhas_cruas = re.findall(r'<text[^>]*font="6"[^>]*>(.*?)</text>', texto)

dicionario_interno = {}
chave_pendente = None # Buffer para armazenar chaves que se encontrem separadas do seu valor

for linha in linhas_cruas:
    # Normalização da string: conversão de entidades HTML e remoção de espaços nas extremidades
    linha = linha.replace("&amp;", "&").strip()
    
    if not linha:
        continue
        
    # Se a linha tiver 2 ou mais espaços consecutivos no meio, ela tem a chave e o valor colados!
    # O re.split corta exatamente por esses espaços múltiplos.
    partes = re.split(r'\s{2,}', linha)
    
    if len(partes) >= 2:
        # Caso A: A linha contém a chave e a descrição
        dicionario_interno[partes[0].strip()] = partes[1].strip()
    else:
        # Caso B: A chave e a descrição foram divididas em tags sucessivas
        if chave_pendente is None:
            # Atribuir a string atual ao buffer (corresponde à chave)
            chave_pendente = linha
        else:
            # Mapear a string atual (descrição) à chave em buffer e redefinir a variável de estado
            dicionario_interno[chave_pendente] = linha
            chave_pendente = None 

# ==========================================
# ESTRUTURA E EXPORTAÇÃO
# ==========================================

json_final = {
    "Abreviaturas": dicionario_interno
}

caminho_json = 'jsons_temporarios/abreviaturas_wipo.json'

with open(caminho_json, "w", encoding="utf-8") as f_out:
    json.dump(json_final, f_out, ensure_ascii=False, indent=4)

print(f"Processamento limpo concluído! Foram extraídas {len(dicionario_interno)} abreviaturas.")