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

# =========================================================================
# UNIR CONCEITOS PARTIDOS EM VÁRIAS LINHAS
# Se um <b> fecha e a linha seguinte abre um <b> que não começa por um número, apagamos as tags do meio e unimos as duas partes com um espaço
# (Corremos duas vezes para garantir que cola conceitos partidos em 3 linhas)
# =========================================================================
texto = re.sub(r'</b>\s*</text>\s*<text[^>]*>\s*<b>\s*(?!\d+\s+)', ' ', texto)
texto = re.sub(r'</b>\s*</text>\s*<text[^>]*>\s*<b>\s*(?!\d+\s+)', ' ', texto)

# 1. MARCAR O CONCEITO PRINCIPAL (2 CASOS DE FORMATAÇÃO NO XML):
# CASO A: O número está DENTRO da tag <b> 
texto = re.sub(r'<text[^>]*>\s*<b>\s*(\d+)\s+(.*?)\s*</b>\s*</text>', r'@@CONCEITO:\1|\2@@', texto)

# CASO B: O número ficou numa tag <text> separada imediatamente do <b>
texto = re.sub(r'<text[^>]*>\s*(\d+)\s*</text>\s*<text[^>]*>\s*<b>\s*(.*?)\s*</b>\s*</text>', r'@@CONCEITO:\1|\2@@', texto)

# 1.1 LIMPAR A CLASSE GRAMATICAL DO CONCEITO:
# Capturamos o ID e o Nome no Grupo 1, e ignoramos o espaço e a classe no final
# Executamos duas vezes para o caso de haverem duas classes seguidas
texto = re.sub(r'(\d+\|.*?)\s+(?:m|f|a|m\s+pl|f\s+pl|pl|s|sg|abrev\.?)@@', r'\1@@', texto)
texto = re.sub(r'(\d+\|.*?)\s+(?:m|f|a|m\s+pl|f\s+pl|pl|s|sg|abrev\.?)@@', r'\1@@', texto)

# 1.2 MARCAR CONCEITOS EXTRA/SECUNDÁRIOS COMO LIXO:
# Qualquer tag <b> que não comece por um número é transformada numa "parede"
texto = re.sub(r'<text[^>]*>\s*<b>\s*(?!\d+\s+)(.*?)\s*</b>\s*</text>', r'@@LIXO:', texto)


# 2. MARCAR A CATEGORIA:
# A maioria está na font="21". As que estão na font="22" (erro do PDF) começam sempre por Maiúscula,
# o que as distingue das traduções que começam por minúscula.
texto = re.sub(r'<text[^>]*font="21"[^>]*>\s*<i>\s*(.*?)\s*</i>\s*</text>', r'@@CATEGORIA:\1@@', texto)
texto = re.sub(r'<text[^>]*font="22"[^>]*>\s*<i>\s*([A-ZÁÉÍÓÚÑÇ].*?)\s*</i>\s*</text>', r'@@CATEGORIA:\1@@', texto)

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

start_match = re.search(r'@@CONCEITO:1\|á\s*@@', texto)
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
    # 1. Extrair o ID e o Conceito
    conceito_match = re.search(r'^(\d+)\|(.*?)@@', bloco)
    if not conceito_match:
        continue

    id_conceito = conceito_match.group(1) 
    conceito = conceito_match.group(2).strip()

    if not conceito:
        continue

    # 2. Extrair Categoria 
    categorias_cruas = re.findall(r'@@CATEGORIA:(.*?)@@', bloco)
    categorias = []
    
    for c in categorias_cruas:
        c = c.strip()
        if c: # Se não for uma categoria vazia
            # Cortar quando uma minúscula choca com uma maiúscula
            c_separado = re.sub(r'([a-záéíóúñ])\s+([A-ZÁÉÍÓÚÑ])', r'\1|\2', c)
            # Agora divide pelo símbolo | que acabámos de criar
            partes = c_separado.split('|')
            categorias.extend(partes) 
            
    if not categorias:
        categorias = "Categoria não identificada"
    
    # 3. Extrair Sinónimos (SIN)
    sin_match = re.search(r'@@SIN:(.*?)(?=@@|$)', bloco)
    sinonimos = [s.strip() for s in sin_match.group(1).split(';')] if sin_match else []
    if not sinonimos:
        sinonimos = "Sinónimos não identificados"

    # 4. Extrair Variantes (VAR)
    var_match = re.search(r'@@VAR:(.*?)(?=@@|$)', bloco)
    variantes = [v.strip() for v in var_match.group(1).split(';')] if var_match else []
    if not variantes:
        variantes = "Variantes não identificadas"
    
    # 5. Extrair Nota/Descrição
    nota_match = re.search(r'@@NOTA:(.*?)(?=@@|$)', bloco)
    nova_descricao = nota_match.group(1).strip() if nota_match else "Descrição não identificada"
    
    # 6. Extrair Traduções
    traducoes = {}
    idiomas = [("ES", "@@ES:"), ("EN", "@@EN:"), ("PT", "@@PT:"), ("LA", "@@LA:")]
    for lang, tag in idiomas:
        # A captura para sempre que encontra o próximo @@ ou o fim da string
        lang_match = re.search(rf'{tag}(.*?)(?=@@|$)', bloco)
        if lang_match:
            # Limpa o texto e normaliza a pontuação
            traducao_limpa = lang_match.group(1).strip().replace(" ; ", "; ")
            traducoes[lang] = traducao_limpa
    if not traducoes:
        traducoes = "Traduções não identificadas"

    # ==========================================================
    # FILTRO ANTI-LIXO (Falsos Positivos de Números de Página)
    # ==========================================================

    # Se não tem categoria nem traduções, é 100% garantido que é um número de página perdido.
    if categorias == "Categoria não identificada" and traducoes == "Traduções não identificadas":
        continue

    # ==========================================================
    # ESTRUTURA DOS DADOS EM JSON C/ TRATAMENTO DE REPETIÇÕES E HOMONÍMIA
    # ==========================================================

    # Primeiro, procurar todas as chaves existentes no dicionário que derivem deste conceito
    chaves_existentes = []
    if conceito in dicionario_medicina:
        chaves_existentes.append(conceito)
    for k in dicionario_medicina.keys():
        if re.match(rf'^\(\d+\)\s+{re.escape(conceito)}$', k):
            chaves_existentes.append(k)
            
    if not chaves_existentes:
        # É a primeira vez que vemos o conceito, guardamos normalmente
        dicionario_medicina[conceito] = {
            "categoria": categorias,
            "sinonimos": sinonimos,
            "variantes": variantes,
            "descricao": nova_descricao,
            "traducoes": traducoes
        }
    else:
        # O conceito já existe! Vamos verificar se faz match perfeito com algum dos existentes
        chave_correspondente = None
        for chave in chaves_existentes:
            dados_existentes = dicionario_medicina[chave]
            if (dados_existentes["categoria"] == categorias and 
                dados_existentes["sinonimos"] == sinonimos and 
                dados_existentes["variantes"] == variantes and 
                dados_existentes["traducoes"] == traducoes):
                chave_correspondente = chave
                break
                
        if chave_correspondente:
            # Se os parâmetros são iguais, e a nova descrição for válida e diferente, fundimos as descrições
            desc_atual = dicionario_medicina[chave_correspondente]["descricao"]
            
            if nova_descricao != "Descrição não identificada" and nova_descricao not in desc_atual:
                
                if desc_atual == "Descrição não identificada":
                    dicionario_medicina[chave_correspondente]["descricao"] = nova_descricao
                
                elif not desc_atual.startswith("(1)"):
                    dicionario_medicina[chave_correspondente]["descricao"] = f"(1) {desc_atual} (2) {nova_descricao}"
                
                else:
                    qtd_existentes = len(re.findall(r'\(\d+\)', desc_atual))
                    dicionario_medicina[chave_correspondente]["descricao"] = f"{desc_atual} ({qtd_existentes + 1}) {nova_descricao}"
        
        else:
            # Se os parâmetros forem diferentes (Homonímia) -> Criar "(1) ..." e "(2) ..."
            if conceito in chaves_existentes:
                dicionario_medicina[f"(1) {conceito}"] = dicionario_medicina.pop(conceito) 
                chaves_existentes.remove(conceito)
                chaves_existentes.append(f"(1) {conceito}")
                
            proximo_numero = len(chaves_existentes) + 1
            nova_chave = f"({proximo_numero}) {conceito}"
            
            dicionario_medicina[nova_chave] = {
                "categoria": categorias,
                "sinonimos": sinonimos,
                "variantes": variantes,
                "descricao": nova_descricao,
                "traducoes": traducoes
            }

# ==========================================
# FASE 3: EXPORTAR PARA JSON
# ==========================================

with open("jsons_temporarios/medicina.json", "w", encoding="utf-8") as f_out:
    json.dump(dicionario_medicina, f_out, ensure_ascii=False, indent=4)

print(f"Processamento limpo concluído! Foram extraídos {len(dicionario_medicina)} conceitos.")

