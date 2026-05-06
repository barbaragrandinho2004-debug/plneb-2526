import re
import json

# 1. Abrir e ler o ficheiro XML completo
caminho_xml = 'dados/medicina.xml'

with open(caminho_xml, 'r', encoding='utf-8') as f:
    texto = f.read()

# ==========================================
# CORTAR AS EXTREMIDADES DO DOCUMENTO:
# ==========================================

# Cortar tudo o que está para trás do título das abreviaturas
start_match = re.search(r'<b>Abreviaturas empregadas</b>', texto)
if start_match:
    texto = texto[start_match.start():]

# Cortar tudo o que está para a frente do início do dicionário
end_match = re.search(r'<b>Vocabulario de medicina</b>', texto, flags=re.IGNORECASE)
if end_match:
    texto = texto[:end_match.start()]

# ==========================================
# EXTRAÇÃO E PROCESSAMENTO DOS DADOS
# ==========================================

#As chaves estão sempre na posição left="174" e as descrições na posição left="259", então basta extrair tudo o que está entre essas tags para obter os pares chave-descrição. 
chaves_cruas = re.findall(r'<text[^>]*left="174"[^>]*>(.*?)</text>', texto)
descricoes_cruas = re.findall(r'<text[^>]*left="259"[^>]*>(.*?)</text>', texto)

# Montar o dicionário interno
dicionario_interno = {}
for chave, descricao in zip(chaves_cruas, descricoes_cruas):
    dicionario_interno[chave.strip()] = descricao.strip()

# Estrutura final com a chave principal
json_final = {
    "Abreviaturas": dicionario_interno
}

# ==========================================
# EXPORTAÇÃO
# ==========================================

caminho_json = 'jsons_temporarios/abreviaturas_medicina.json'

with open(caminho_json, "w", encoding="utf-8") as f_out:
    json.dump(json_final, f_out, ensure_ascii=False, indent=4)

print(f"Processamento limpo concluído! Foram extraídas {len(dicionario_interno)} abreviaturas.")