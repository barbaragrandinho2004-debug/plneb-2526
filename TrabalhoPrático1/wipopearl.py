import re
import json

# 1. Definir o caminho do ficheiro XML de origem
caminho_xml = r'C:\Users\barba\OneDrive - Universidade do Minho\Universidade\4ºano\2º Semestre\PLN\plneb-2526\TrabalhoPrático1\dados\wipopearl_covid.xml'

with open(caminho_xml, 'r', encoding='utf-8') as f:
    texto = f.read()

# Normalização inicial: o XML codifica o "&" como "&amp;". Vamos limpar isso.
texto = texto.replace("&amp;", "&")

# =========================================================================
# CORTAR AS EXTREMIDADES DO DOCUMENTO 
# =========================================================================

# Cortar tudo o que está para trás do título do glossário
start_match = re.search(r'<b>Multilingual Glossary </b>', texto)
if start_match:
    texto = texto[start_match.end():]

# Cortar o rodapé final comum da última página para excluir os metadados
end_match = re.search(r'World Intellectual Property Organization', texto)
if end_match:
    texto = texto[:end_match.start()]

# =========================================================================
# FASE 1: LIMPEZA DE DADOS E MARCAÇÕES TÁTICAS
# =========================================================================

# Remover tags estruturais desnecessárias que sujam o texto
texto = re.sub(r'</?page.*?>', '', texto)
texto = re.sub(r'</?fontspec.*?>', '', texto)

# 1. MARCAR O CONCEITO: Sabemos pelo PDF que os conceitos base estão sempre na font 8 a negrito
texto = re.sub(r'<text[^>]*font="8"[^>]*>\s*<b>\s*(.*?)\s*</b>\s*</text>', r'@@CONCEITO:\1@@', texto)

# 2. MARCAR A CATEGORIA: As categorias estão sempre na font 11.
texto = re.sub(r'<text[^>]*font="11"[^>]*>\s*(.*?)\s*</text>', r'@@CATEGORIA:\1@@', texto)

# 3. MARCAR DESCRIÇÃO: O texto da descrição usa a font 6. 
# Como as descrições ocupam várias linhas, marcamos cada linha individualmente. Na Fase 2 vamos colá-las.
texto = re.sub(r'<text[^>]*font="6"[^>]*>\s*(.*?)\s*</text>', r'@@DESC:\1@@', texto)

# 4. MARCAR IDIOMAS: As siglas das línguas estão na font 7 a negrito.
# Capturamos apenas as siglas oficiais para evitar falsos positivos
texto = re.sub(r'<text[^>]*font="7"[^>]*>\s*<b>\s*(AR|DE|ES|FR|JA|KO|PT|RU|ZH)\s*</b>\s*</text>', r'@@LANG:\1@@', texto)


# 5. LIMPEZA FINAL DO XML: Remoção de tags XML residuais e normalização de espaços em branco consecutivos.
texto = re.sub(r'<[^>]+>', ' ', texto) 
texto = re.sub(r'\s+', ' ', texto)

# =========================================================================
# FASE 2: EXTRAÇÃO E ESTRUTURAÇÃO
# =========================================================================

dicionario_wipo = {}

# Ignorar o índice [0] porque é o espaço vazio antes do primeiro conceito
blocos = texto.split("@@CONCEITO:")[1:]

for bloco in blocos:
    # 1. Extrair o Conceito Base
    # O conceito está logo no início do bloco, até ao primeiro "@@"
    conceito_match = re.search(r'^(.*?)@@', bloco)
    if not conceito_match:
        continue

    conceito = conceito_match.group(1).strip()
    # Guardamos o resto do bloco (tudo o que vem depois do conceito) para pesquisar
    bloco_restante = bloco[conceito_match.end():] 

    # 2. Extrair Categorias
    cat_match = re.search(r'@@CATEGORIA:(.*?)@@', bloco_restante)
    if cat_match:
        # As categorias neste documento vêm separadas por vírgula
        categorias = [c.strip() for c in cat_match.group(1).split(',')]
    else:
        categorias = ["Categoria não identificada"]

    # 3. Extrair Descrição
    # Encontramos todas as linhas marcadas com @@DESC: e unimos com um espaço
    desc_matches = re.findall(r'@@DESC:(.*?)@@', bloco_restante)
    nova_descricao = " ".join([d.strip() for d in desc_matches]).strip()
    if not nova_descricao:
        nova_descricao = "Descrição não identificada"

    # 4. Extrair Sinónimos Principais 
    # Para não extrair os (syn.) das traduções, isolamos apenas a string que existe entre o conceito e o início da Descrição ou da Categoria (o "cabeçalho").
    desc_pos = bloco_restante.find("@@DESC:")
    cat_pos = bloco_restante.find("@@CATEGORIA:")
    
    limites = [pos for pos in [desc_pos, cat_pos] if pos != -1]
    limite_header = min(limites) if limites else len(bloco_restante)
    
    # "header" contém apenas o espaço onde mora o sinónimo inglês
    header = bloco_restante[:limite_header]
    
    # Procuramos literalmente pela palavra (syn.) apenas no cabeçalho
    sin_match = re.search(r'\(syn\.\)\s*(.*)', header)
    if sin_match:
        sin_raw = sin_match.group(1).strip()
        sinonimos = [s.strip() for s in sin_raw.split(',') if s.strip()]
    else:
        sinonimos = "Sinónimos não identificados"

    # 5. Extrair Traduções
    traducoes = {}
    # O re.split divide a string sempre que encontra um idioma.
    # Exemplo de output: ['texto solto', 'ES', 'tradução espanhola', 'PT', 'tradução PT']
    partes_lang = re.split(r'@@LANG:([A-Z]{2})@@', bloco_restante)
    
    # Saltamos o índice 0 e iteramos de 2 em 2 (Código do idioma -> Texto da tradução)
    for i in range(1, len(partes_lang), 2):
        lang_code = partes_lang[i]
        lang_text = partes_lang[i+1].strip()
        
        # O lang_text mantém-se 100% fiel ao original (incluindo as vírgulas e os "(syn.)" que possam ter)
        if lang_text:
            traducoes[lang_code] = lang_text
            
    if not traducoes:
        traducoes = "Traduções não identificadas"

    # =========================================================================
    # LÓGICA DE FUSÃO E HOMONÍMIA
    # =========================================================================

    chaves_existentes = []
    if conceito in dicionario_wipo:
        chaves_existentes.append(conceito)
    for k in dicionario_wipo.keys():
        if re.match(rf'^\(\d+\)\s+{re.escape(conceito)}$', k):
            chaves_existentes.append(k)
            
    if not chaves_existentes:
        # É a primeira vez que vemos o conceito, guardamos normalmente
        dicionario_wipo[conceito] = {
            "categoria": categorias,
            "sinonimos": sinonimos,
            "descricao": nova_descricao,
            "traducoes": traducoes
        }
    else:
        # O conceito já existe! Procurar correspondência de parâmetros
        chave_correspondente = None
        for chave in chaves_existentes:
            dados_existentes = dicionario_wipo[chave]
            if (dados_existentes["categoria"] == categorias and 
                dados_existentes["sinonimos"] == sinonimos and 
                dados_existentes["traducoes"] == traducoes):
                chave_correspondente = chave
                break
                
        if chave_correspondente:
            # Fundir as notas explicativas se forem diferentes
            desc_atual = dicionario_wipo[chave_correspondente]["descricao"]
            if nova_descricao != "Descrição não identificada" and nova_descricao not in desc_atual:
                if desc_atual == "Descrição não identificada":
                    dicionario_wipo[chave_correspondente]["descricao"] = nova_descricao
                elif not desc_atual.startswith("(1)"):
                    dicionario_wipo[chave_correspondente]["descricao"] = f"(1) {desc_atual} (2) {nova_descricao}"
                else:
                    qtd_existentes = len(re.findall(r'\(\d+\)', desc_atual))
                    dicionario_wipo[chave_correspondente]["descricao"] = f"{desc_atual} ({qtd_existentes + 1}) {nova_descricao}"
        else:
            # Homonímia -> Os conceitos são iguais, mas categorias/traduções diferentes.
            if conceito in chaves_existentes:
                dicionario_wipo[f"(1) {conceito}"] = dicionario_wipo.pop(conceito) 
                chaves_existentes.remove(conceito)
                chaves_existentes.append(f"(1) {conceito}")
                
            proximo_numero = len(chaves_existentes) + 1
            nova_chave = f"({proximo_numero}) {conceito}"
            
            dicionario_wipo[nova_chave] = {
                "categoria": categorias,
                "sinonimos": sinonimos,
                "descricao": nova_descricao,
                "traducoes": traducoes
            }

# =========================================================================
# FASE 3: EXPORTAÇÃO JSON
# =========================================================================


with open("jsons_temporarios/wipopearl.json", "w", encoding="utf-8") as f_out:
    json.dump(dicionario_wipo, f_out, ensure_ascii=False, indent=4)

print(f"Processamento limpo concluído com sucesso! Foram extraídos {len(dicionario_wipo)} conceitos.")