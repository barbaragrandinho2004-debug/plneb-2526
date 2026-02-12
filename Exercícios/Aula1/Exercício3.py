#Exercício3

#Função que recebe nome de ficheiro e imprime linhas do ficheiro em ordem inversa
def imprime_linhas_inversas(nome_ficheiro):
    with open(nome_ficheiro, 'r') as f:
        linhas = f.readlines()
        for linha in reversed(linhas):
            print(linha.strip())