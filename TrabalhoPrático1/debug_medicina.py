import re

# 1. Abrir e ler o ficheiro XML
with open(r'C:\Users\barba\OneDrive - Universidade do Minho\Universidade\4ºano\2º Semestre\PLN\plneb-2526\TrabalhoPrático1\dados\medicina.xml', 'r', encoding='utf-8') as f:
    texto = f.read()

# Remover lixo
texto = re.sub(r'</?page.*?>', '', texto)
texto = re.sub(r'</?fontspec.*?>', '', texto)

# Cortar as extremidades (para ser igualzinho ao script oficial)
start_match = re.search(r'<text[^>]*>\s*<b>\s*1\s+á', texto)
if start_match:
    texto = texto[start_match.start():]

end_match = re.search(r'Í\s*ndice\s+de\s+denominacións', texto, flags=re.IGNORECASE)
if end_match:
    texto = texto[:end_match.start()]

# 2. AS NOSSAS EXPRESSÕES REGULARES (Agora guardam o ID na \1 e o Nome na \2)
# CASO A:
texto = re.sub(r'<text[^>]*>\s*<b>\s*(\d+)\s+(.*?)\s*</b>\s*</text>', r'@@CONCEITO:\1|\2@@', texto)
# CASO B:
texto = re.sub(r'<text[^>]*>\s*(\d+)\s*</text>\s*<text[^>]*>\s*<b>\s*(.*?)\s*</b>\s*</text>', r'@@CONCEITO:\1|\2@@', texto)

# 3. EXTRAÇÃO PARA VERIFICAR OS IDS
blocos = texto.split("@@CONCEITO:")[1:]
ids_extraidos = set()

for bloco in blocos:
    # Procura o ID e o Conceito no início do bloco
    match = re.search(r'^(\d+)\|(.*?)@@', bloco)
    if match:
        ids_extraidos.add(int(match.group(1)))

# 4. ENCONTRAR OS DESAPARECIDOS
conceitos_em_falta = []
for i in range(1, 5394):
    if i not in ids_extraidos:
        conceitos_em_falta.append(i)

print(f"Sucesso! Extraímos {len(ids_extraidos)} conceitos.")
print(f"Faltam {len(conceitos_em_falta)} conceitos. São eles:")
print(conceitos_em_falta)