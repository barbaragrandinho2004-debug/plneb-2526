def conta_ocorrencias(s1,s2):
    contador = 0
    for i in range(len(s2)-len(s1)+1):
        if s2[i:i+len(s1)] == s1:
            contador += 1
    return contador

print(conta_ocorrencias("ana", "banana"))
print(conta_ocorrencias("ule", "chule"))