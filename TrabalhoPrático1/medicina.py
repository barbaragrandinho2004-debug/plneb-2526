# medicina_parser.py
import re

def extrair_termos(caminho_xml):
    """
    Processa o ficheiro XML e devolve uma lista de dicionários.
    """
    print(f"[{caminho_xml}] A iniciar extração...")
    
    # 1. Abrir o ficheiro convertido
    with open(caminho_xml, 'r', encoding='utf-8') as f:
        texto_xml = f.read()
        
    lista_de_conceitos = []
    
    # =========================================================
    # ESPAÇO PARA A MAGIA DAS EXPRESSÕES REGULARES (REGEX)
    # É aqui que vamos trabalhar assim que me enviares o XML!
    # =========================================================
    
    # Exemplo mock (só para testar a ligação com o main.py):
    # lista_de_conceitos.append({
    #     "termo": "Termo Falso", 
    #     "definicao": "Definição Falsa para testar o código."
    # })
    
    # =========================================================
    
    print(f"[{caminho_xml}] Extraídos {len(lista_de_conceitos)} termos.")
    return lista_de_conceitos