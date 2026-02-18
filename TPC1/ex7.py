def strings_balanceadas(s1, s2):
    for caracter in s1:
        if caracter not in s2:
            return False
    return True

print(strings_balanceadas("abc", "cbadef"))