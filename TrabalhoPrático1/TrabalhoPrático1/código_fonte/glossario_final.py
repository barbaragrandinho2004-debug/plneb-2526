import json
import re
import os

# =========================================================================
# FUNÇÕES AUXILIARES
# =========================================================================

def normalizar_conceito(dados_originais):
    """
    Aplica o 'Molde' a um conceito. Se o conceito original não tiver uma chave,
    ela é criada com o valor de defeito para garantir coerência estrutural (Schema Enforcement).
    """
    molde = {
        "categoria": "Categoria não identificada",
        "sinonimos": "Sinónimos não identificados",
        "variantes": "Variantes não identificadas",
        "descricao": "Descrição não identificada",
        "traducoes": "Traduções não identificadas"
    }
    
    conceito_normalizado = {}
    for chave, valor_defeito in molde.items():
        # Se a chave existir no original e não for uma lista vazia ou string vazia, mantém.
        # Caso contrário, aplica o valor por defeito.
        if chave in dados_originais and dados_originais[chave] and dados_originais[chave] != []:
            conceito_normalizado[chave] = dados_originais[chave]
        else:
            conceito_normalizado[chave] = valor_defeito
            
    return conceito_normalizado

def adicionar_ao_dicionario(dicionario_destino, conceito, dados_novos):
    """
    Insere o conceito no dicionário final. Trata automaticamente repetições:
    - Funde as descrições se todos os outros parâmetros forem idênticos.
    - Cria homónimos (ex: (1) conceito, (2) conceito) se vierem de línguas/estruturas diferentes.
    """
    chaves_existentes = []
    
    if conceito in dicionario_destino:
        chaves_existentes.append(conceito)
    for k in dicionario_destino.keys():
        if re.match(rf'^\(\d+\)\s+{re.escape(conceito)}$', k):
            chaves_existentes.append(k)
            
    if not chaves_existentes:
        # Inserção limpa: primeira vez que vemos o conceito
        dicionario_destino[conceito] = dados_novos
    else:
        # O conceito já existe. Vamos verificar se faz match com algum existente
        chave_correspondente = None
        for chave in chaves_existentes:
            dados_existentes = dicionario_destino[chave]
            if (dados_existentes["categoria"] == dados_novos["categoria"] and 
                dados_existentes["sinonimos"] == dados_novos["sinonimos"] and 
                dados_existentes["variantes"] == dados_novos["variantes"] and 
                dados_existentes["traducoes"] == dados_novos["traducoes"]):
                chave_correspondente = chave
                break
                
        if chave_correspondente:
            # Match perfeito: Fundir descrições
            desc_atual = dicionario_destino[chave_correspondente]["descricao"]
            nova_descricao = dados_novos["descricao"]
            
            if nova_descricao != "Descrição não identificada" and nova_descricao not in desc_atual:
                if desc_atual == "Descrição não identificada":
                    dicionario_destino[chave_correspondente]["descricao"] = nova_descricao
                elif not desc_atual.startswith("(1)"):
                    dicionario_destino[chave_correspondente]["descricao"] = f"(1) {desc_atual} (2) {nova_descricao}"
                else:
                    qtd_existentes = len(re.findall(r'\(\d+\)', desc_atual))
                    dicionario_destino[chave_correspondente]["descricao"] = f"{desc_atual} ({qtd_existentes + 1}) {nova_descricao}"
        else:
            # Homonímia (origens/línguas diferentes): separar em (1), (2), etc.
            if conceito in chaves_existentes:
                dicionario_destino[f"(1) {conceito}"] = dicionario_destino.pop(conceito) 
                chaves_existentes.remove(conceito)
                chaves_existentes.append(f"(1) {conceito}")
                
            proximo_numero = len(chaves_existentes) + 1
            nova_chave = f"({proximo_numero}) {conceito}"
            
            dicionario_destino[nova_chave] = dados_novos


# =========================================================================
# FASE 1: CARREGAR OS 4 FICHEIROS JSON
# =========================================================================


caminhos_conceitos = {
    "medicina": "jsons_temporarios/medicina.json",
    "wipo": "jsons_temporarios/wipopearl.json",
    "neologismos": "jsons_temporarios/neologismos_temp.json",
    "ministerio": "jsons_temporarios/ministerio_saude_temp.json",
    }
    
caminho_siglas = "jsons_temporarios/siglas_geral.json"
caminho_abreviaturas = "jsons_temporarios/abreviaturas_gerais.json"

# Carregar os dados específicos de siglas e abreviaturas
with open(caminho_siglas, 'r', encoding='utf-8') as f:
    dados_siglas = json.load(f).get("Siglas", {})

with open(caminho_abreviaturas, 'r', encoding='utf-8') as f:
    dados_abreviaturas = json.load(f).get("Abreviaturas", {})


dicionarios_brutos = []

for nome, caminho in caminhos_conceitos.items():
    if os.path.exists(caminho):
        with open(caminho, 'r', encoding='utf-8') as f:
            dicionarios_brutos.append(json.load(f))
            print(f"[{nome}] carregado com sucesso.")
    else:
        print(f"ERRO: Não foi possível encontrar o ficheiro {caminho}")

# =========================================================================
# FASE 2: UNIFICAÇÃO DOS CONCEITOS
# =========================================================================

conceitos_finais = {}

for dic in dicionarios_brutos:
    for conceito, dados in dic.items():
        # 1. Normalizar as chaves em falta aplicando o 'Molde'
        dados_normalizados = normalizar_conceito(dados)
        
        # 2. Inserir no dicionário final (gerindo conflitos/fusões)
        adicionar_ao_dicionario(conceitos_finais, conceito, dados_normalizados)

# =========================================================================
# FASE 3: CONSTRUÇÃO DA ÁRVORE DO GLOSSÁRIO GERAL
# =========================================================================

# A estrutura final pedida, preparada para receber as siglas e abreviaturas
glossario_geral = {
    "Glossário de Medicina e Saúde": {
        "Siglas": dados_siglas,        
        "Abreviaturas": dados_abreviaturas, 
        "Conceitos": conceitos_finais
    }
}

# Exportar o Glossário Final
caminho_final = "glossario_final.json"

with open(caminho_final, "w", encoding="utf-8") as f_out:
    json.dump(glossario_geral, f_out, ensure_ascii=False, indent=4)

print(f"O glossario_final.json foi gerado com sucesso.")
print(f"Total de conceitos únicos alojados: {len(conceitos_finais)}")