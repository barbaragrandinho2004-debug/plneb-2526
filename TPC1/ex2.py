def contar_as(s):
    contador = 0
    for l in s.lower():
        if l == 'a':
            contador += 1
    return contador

print(contar_as("Andreia"))