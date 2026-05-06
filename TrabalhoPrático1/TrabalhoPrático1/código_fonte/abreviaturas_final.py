import json

def unificar_multiplas_abreviaturas(lista_ficheiros, ficheiro_saida):
    print("A iniciar a unificação de todas as Abreviaturas...")
    
    abrevs_unificadas = {}
    chaves_repetidas_evitadas = 0

    # 1. Percorrer todos os ficheiros da lista de abreviaturas
    for ficheiro in lista_ficheiros:
        try:
            with open(ficheiro, 'r', encoding='utf-8') as f:
                dados = json.load(f)
                abrevs_temporarias = dados.get("Abreviaturas", {})
                
                # 2. Lógica anti-repetição
                for chave, significado in abrevs_temporarias.items():
                    # Se a chave já existir no dicionário principal, ignoramos a nova
                    if chave in abrevs_unificadas:
                        chaves_repetidas_evitadas += 1
                    else:
                        # Se for uma chave nova, adicionamos
                        abrevs_unificadas[chave] = significado
                        
        except FileNotFoundError:
            print(f"Aviso: Não encontrei o ficheiro '{ficheiro}'. Vou saltar este ficheiro.")

    # 3. Ordenar alfabeticamente (ignorando maiúsculas e minúsculas)
    abrevs_ordenadas = dict(sorted(abrevs_unificadas.items(), key=lambda item: item[0].lower()))

    # 4. Envolver o resultado final na chave principal "Abreviaturas"
    json_final = {
        "Abreviaturas": abrevs_ordenadas
    }

    # 5. Exportar para o ficheiro JSON final
    with open(ficheiro_saida, 'w', encoding='utf-8') as f_out:
        json.dump(json_final, f_out, indent=4, ensure_ascii=False)

    print(f"\n--- Resumo da Unificação ---")
    print(f"Total de ficheiros lidos: {len(lista_ficheiros)}")
    print(f"Repetições evitadas: {chaves_repetidas_evitadas}")
    print(f"Sucesso! O ficheiro final '{ficheiro_saida}' tem {len(abrevs_ordenadas)} abreviaturas únicas.")


meus_ficheiros = [
    "jsons_temporarios/abreviaturas_medicina.json", 
    "jsons_temporarios/abreviaturas_wipo.json", 
    "jsons_temporarios/abreviaturas_neologismos.json"  
]

unificar_multiplas_abreviaturas(
    lista_ficheiros=meus_ficheiros,
    ficheiro_saida="jsons_temporarios/abreviaturas_gerais.json"
)