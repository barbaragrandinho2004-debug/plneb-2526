#Exercício2

def imprime_pares():
    lista=[]
    while True:
        num = int(input("Digite um número inteiro (ou -1 para sair): "))
        if num == -1:
            break
        if num % 2 == 0:
            lista.append(num)
    print(lista)

imprime_pares()


    