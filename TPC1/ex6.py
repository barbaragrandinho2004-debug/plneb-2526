def verifica_capicua(s):
    s_limpa = s.lower().replace(" ", "")
    reversa = s_limpa[::-1]
    if s_limpa == reversa:
        return True
    else:
        return False

print(verifica_capicua("2002"))
print(verifica_capicua("2026"))
print(verifica_capicua("A amor Roma a"))