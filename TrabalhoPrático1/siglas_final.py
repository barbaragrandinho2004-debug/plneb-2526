import json

def unificar_siglas_estruturadas(ficheiro_ministerio, ficheiro_neologismos, ficheiro_neologismos_embutido, ficheiro_saida):
    print("A iniciar a unificação das Siglas...")
    
    siglas_unificadas = {}
    repeticoes_evitadas = 0

    # ==========================================
    # 1. Carregar o ficheiro das siglas Ministério da Saúde
    # ==========================================
    try:
        with open(ficheiro_ministerio, 'r', encoding='utf-8') as f:
            dados_ms = json.load(f)
            # Extraímos apenas o conteúdo dentro da chave "Siglas"
            conteudo_ms = dados_ms.get("Siglas", {})
            
            for chave, significado in conteudo_ms.items():
                siglas_unificadas[chave] = significado
    except FileNotFoundError:
        print(f"Aviso: Ficheiro '{ficheiro_ministerio}' não encontrado.")
        conteudo_ms = {}

    # ==========================================
    # 2. Carregar o ficheiro das siglas Neologismos
    # ==========================================

    try:
        with open(ficheiro_neologismos, 'r', encoding='utf-8') as f:
            dados_neo = json.load(f)
            # Extraímos apenas o conteúdo dentro da chave "Siglas"
            conteudo_neo = dados_neo.get("Siglas", {})
            
            for chave, significado in conteudo_neo.items():
                # Verificação de duplicados: se já existe, ignoramos para não repetir
                if chave in siglas_unificadas:
                    repeticoes_evitadas += 1
                else:
                    siglas_unificadas[chave] = significado
    except FileNotFoundError:
        print(f"Aviso: Ficheiro '{ficheiro_neologismos}' não encontrado.")
        conteudo_neo = {}

    # ==========================================
    # 3. Carregar o ficheiro das siglas do Neologismos embutidas
    # ==========================================
    try:
        with open(ficheiro_neologismos_embutido, 'r', encoding='utf-8') as f:
            dados_neo_embutido = json.load(f)
            # Extraímos apenas o conteúdo dentro da chave "Siglas"
            conteudo_neo_embutido = dados_neo_embutido.get("Siglas", {})
            
            for chave, significado in conteudo_neo_embutido.items():
                # Verificação de duplicados: se já existe, ignoramos para não repetir
                if chave in siglas_unificadas:
                    repeticoes_evitadas += 1
                else:
                    siglas_unificadas[chave] = significado
    except FileNotFoundError:
        print(f"Aviso: Ficheiro '{ficheiro_neologismos_embutido}' não encontrado.")
        conteudo_neo = {}

    # ==========================================
    # 3. Ordenar alfabeticamente
    # ==========================================
    siglas_ordenadas = dict(sorted(siglas_unificadas.items(), key=lambda item: item[0].lower()))

    # ==========================================
    # 4. Criar a estrutura final com a chave raiz "Siglas"
    # ==========================================

    json_final = {
        "Siglas": siglas_ordenadas
    }

    # ==========================================
    # 5. Exportar para JSON
    # ==========================================
    
    with open(ficheiro_saida, 'w', encoding='utf-8') as f_out:
        json.dump(json_final, f_out, indent=4, ensure_ascii=False)

    print(f"\n--- Resumo ---")
    print(f"Siglas do Ministério: {len(conteudo_ms)}")
    print(f"Siglas dos Neologismos: {len(conteudo_neo)}")
    print(f"Siglas dos Neologismos Embutidas: {len(conteudo_neo_embutido)}")
    print(f"Duplicados ignorados: {repeticoes_evitadas}")
    print(f"Sucesso! Ficheiro '{ficheiro_saida}' criado com {len(siglas_ordenadas)} siglas únicas.")

# Executar a função 
unificar_siglas_estruturadas(
    ficheiro_ministerio="jsons_temporarios/siglas_ministerio.json",  
    ficheiro_neologismos="jsons_temporarios/siglas_neologismos.json",
    ficheiro_neologismos_embutido="jsons_temporarios/siglas_embutidas_neologismos.json",            
    ficheiro_saida="jsons_temporarios/siglas_geral.json"  
)