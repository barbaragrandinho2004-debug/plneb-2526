def conta_vogais(s):
    contador = 0
    vogais = 'aeiouAEIOUáéíóúÁÉÍÓÚâêîôûÂÊÎÔÛãõÃÕàèìòùÀÈÌÒÙ'
    for l in s:
        if l in vogais:
            contador += 1
    return contador

print(conta_vogais('Olá, bom dia!')) 
print(conta_vogais('Conceição'))   