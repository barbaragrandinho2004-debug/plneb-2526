def reverter_string(s):
    string_invertida=""
    for l in s[::-1]: 
        string_invertida += l
    
    return string_invertida

print(reverter_string("Bom dia"))