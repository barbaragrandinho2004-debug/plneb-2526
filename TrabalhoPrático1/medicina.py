import re
import json

# 1. Abrir e ler o ficheiro XML
with open(r'C:\Users\barba\OneDrive - Universidade do Minho\Universidade\4ºano\2º Semestre\PLN\plneb-2526\TrabalhoPrático1\dados\medicina.xml', 'r', encoding='utf-8') as f:
    texto = f.read()

# ==========================================
# FASE 1: LIMPEZA DE DADOS E MARCAÇÕES
# ==========================================

# Remover lixo de formatação do XML (pages, fontspecs, etc.)
texto = re.sub(r'</?page.*?>', '', texto)
texto = re.sub(r'</?fontspec.*?>', '', texto)

# 1. MARCAR O CONCEITO PRINCIPAL (2 CASOS DE FORMATAÇÃO NO XML):
# CASO A: O número está DENTRO da tag <b> 
texto = re.sub(r'<text[^>]*>\s*<b>\s*\d+\s+(.*?)\s*</b>\s*</text>', r'@@CONCEITO:\1@@', texto)

# CASO B: O número ficou numa tag <text> separada imediatamente do <b> (ex: ácido desoxirribonucleico)
texto = re.sub(r'<text[^>]*>\s*\d+\s*</text>\s*<text[^>]*>\s*<b>\s*(.*?)\s*</b>\s*</text>', r'@@CONCEITO:\1@@', texto)

# 1.1 LIMPAR A CLASSE GRAMATICAL DO CONCEITO:
# Limpamos estritamente as classes (m, f, a, pl, s) antes dos @@ para que o nome fique puro.
# Executamos duas vezes para o caso de haverem duas classes seguidas (ex: "m pl")
texto = re.sub(r'\s+(?:m|f|a|m\s+pl|f\s+pl|pl|s)@@', '@@', texto)
texto = re.sub(r'\s+(?:m|f|a|m\s+pl|f\s+pl|pl|s)@@', '@@', texto)


# 1.1 MARCAR CONCEITOS EXTRA/SECUNDÁRIOS COMO LIXO:
# Qualquer tag <b> que não comece por um número é transformada numa "parede"
texto = re.sub(r'<text[^>]*>\s*<b>\s*(?!\d+\s+)(.*?)\s*</b>\s*</text>', r'@@LIXO:', texto)

# 2. MARCAR A CATEGORIA:
# O XML usa sempre a font="21" para a categoria em itálico
texto = re.sub(r'<text[^>]*font="21"[^>]*>\s*<i>\s*(.*?)\s*</i>\s*</text>', r'@@CATEGORIA:\1@@', texto)

# 3. MARCAR OS IDIOMAS (traduções):
texto = re.sub(r'<text[^>]*>\s*es\s*</text>', r'@@ES:', texto)
texto = re.sub(r'<text[^>]*>\s*en\s*</text>', r'@@EN:', texto)
texto = re.sub(r'<text[^>]*>\s*pt\s*</text>', r'@@PT:', texto)
texto = re.sub(r'<text[^>]*>\s*la\s*</text>', r'@@LA:', texto)

# 4. MARCAR SINÓNIMOS, VARIANTES E NOTAS:
texto = re.sub(r'SIN\.-', '@@SIN:', texto)
texto = re.sub(r'VAR\.-', '@@VAR:', texto)
texto = re.sub(r'Nota\.-', '@@NOTA:', texto)


# 5. LIMPEZA FINAL DO XML:
# Substitui qualquer tag XML restante por um espaço e remove espaços duplicados
texto = re.sub(r'<[^>]+>', ' ', texto) 
texto = re.sub(r'\s+', ' ', texto)

# 6. LIMPAR CABEÇALHOS DE PÁGINA:
texto = re.sub(r'V\s*ocabulario\s*\d*', '@@LIXO:', texto, flags=re.IGNORECASE)

# 7. CORTAR AS EXTREMIDADES DO DOCUMENTO (Introdução e Índices Finais):
start_match = re.search(r'@@CONCEITO:\s*á\s*@@', texto)
if start_match:
    texto = texto[start_match.start():]

end_match = re.search(r'Í\s*ndice\s+de\s+denominacións', texto, flags=re.IGNORECASE)
if end_match:
    texto = texto[:end_match.start()]

# ==========================================
# FASE 2: EXTRAÇÃO DA INFORMAÇÃO
# ==========================================

dicionario_medicina = {}

# O split divide o texto gigante num bloco para cada conceito.
# Ignoramos o índice 0 porque corresponde ao cabeçalho antes do primeiro conceito.
blocos = texto.split("@@CONCEITO:")[1:]

for bloco in blocos:
    # 1. Extrair o Conceito
    conceito_match = re.search(r'^(.*?)@@', bloco)
    if not conceito_match:
        continue
    conceito = conceito_match.group(1).strip()
    
    # 2. Extrair Categorias (em formato de lista para suportar múltiplas ocorrências)
    cat_match = re.search(r'@@CATEGORIA:(.*?)@@', bloco)
    if cat_match:
        cat_raw = cat_match.group(1).strip()
        # Divide a string sempre que encontrar 2 ou mais espaços consecutivos
        categorias = [c.strip() for c in re.split(r'\s{2,}', cat_raw) if c.strip()]
    else:
        categorias = []
    
    # 3. Extrair Sinónimos (SIN)
    sin_match = re.search(r'@@SIN:(.*?)(?=@@|$)', bloco)
    sinonimos = [s.strip() for s in sin_match.group(1).split(';')] if sin_match else []
    
    # 4. Extrair Variantes (VAR)
    var_match = re.search(r'@@VAR:(.*?)(?=@@|$)', bloco)
    variantes = [v.strip() for v in var_match.group(1).split(';')] if var_match else []
    
    # 5. Extrair Nota
    nota_match = re.search(r'@@NOTA:(.*?)(?=@@|$)', bloco)
    nota = nota_match.group(1).strip() if nota_match else "Não existe"
    
    # 6. Extrair Traduções
    traducoes = {}
    idiomas = [("ES", "@@ES:"), ("EN", "@@EN:"), ("PT", "@@PT:"), ("LA", "@@LA:")]
    for lang, tag in idiomas:
        # A captura pára sempre que encontra o próximo @@ (seja idioma, nota, ou o nosso @@LIXO, ou fim da string ($))
        lang_match = re.search(rf'{tag}(.*?)(?=@@|$)', bloco)
        if lang_match:
            # Limpa o texto e normaliza a pontuação
            traducao_limpa = lang_match.group(1).strip().replace(" ; ", "; ")
            traducoes[lang] = traducao_limpa
    

    # Guardar os dados estruturados no dicionário
    dicionario_medicina[conceito] = {
        "categorias": categorias,
        "sinonimos": sinonimos,
        "variantes": variantes,
        "nota": nota,
        "traducoes": traducoes
    }

# ==========================================
# FASE 3: EXPORTAR PARA JSON
# ==========================================

with open("jsons_temporarios/medicina.json", "w", encoding="utf-8") as f_out:
    json.dump(dicionario_medicina, f_out, ensure_ascii=False, indent=4)

print(f"Processamento limpo concluído! Foram extraídos {len(dicionario_medicina)} conceitos.")