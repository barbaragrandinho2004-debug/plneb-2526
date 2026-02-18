Exercício 1:

Criei uma variável vazia (string_invertida = "") onde será guardado o resultado do novo texto.

Utilizei o slicing, cuja sintaxe é a seguinte:

string[início:fim:passo]

Ao omitir o início e o fim e definir o passo como -1, o Python, com o ciclo for percorre a sequência da direita para a esquerda, e adiciona cada letra (l) à variável acumuladora string_invertida criando uma nova cópia invertida da string original.

Exercício 2:

Criei uma variável de suporte à contagem (contador = 0) para registar o número de vezes que a letra aparece durante a verificação.

Para garantir que a contagem é precisa e conta todos os a's tanto minusculos como maiusculos utilizei o método .lower() na string de entrada.

Utilizei um ciclo for para percorrer cada letra (l) da string convertida. Dentro do ciclo, apliquei uma condição (if) para verificar se a letra é igual a 'a'. Se for, o valor da variável contador é incrementado em 1.

No final do ciclo, a função retorna o total acumulado.

Exercício 3:

Criei uma variável de suporte à contagem (contador = 0) para registar o número total de vogais encontradas na string de entrada.

Defini uma variável de referência (vogais) que contém não só as vogais simples, mas também as vogais acentuadas (agudos, circunflexos, tis e graves) em maiúsculas e minúsculas. Isto é fundamental para englobar todas as vogais mesmo que se apresentem com acentos.

Utilizei um ciclo for para percorrer cada caracter (l) da string fornecida. Para cada letra, apliquei uma condição (if) para verificar se a letra está presente (operador de pertença in) no conjunto de vogais. 

Se o caracter atual estiver presente no conjunto de vogais, o valor da variável contador é incrementado em 1.

No final do ciclo, a função retorna o total acumulado.

Exercício 4:

Utilizei o método .lower(), que percorre a string original e, para cada caracter que seja uma letra maiúscula, substitui-o pelo seu equivalente em minúscula.

Exercício 5:´

Utilizei o método .upper(), que percorre a string original e, para cada caracter que seja uma letra minúscula, substitui-o pelo seu equivalente em maiúscula.

Exercício 6:

Preparei a string convertendo-a para minúsculas e removendo espaços com .replace(" ", ""), para que frases complexas sejam validadas corretamente.

Criei uma versão invertida da string e utilizei um operador de comparação (==) para verificar se a original e a invertida são idênticas, retornando um valor booleano (True ou False).

Exercício 7:

Utilizei um ciclo for para percorrer cada caracter individual de s1. Para cada um desses caracteres, apliquei uma estrutura condicional (if) com o operador not in para verificar a sua existência em s2:

-> Se a função encontrar um único caracter em s1 que não existe em s2, ela retorna imediatamente False. Isto torna o código mais eficiente, pois não precisa de verificar os caracteres restantes se a condição já falhou.

-> Se o ciclo percorrer toda a string s1 sem encontrar nenhuma falha, a função sai do ciclo e retorna True, confirmando que as strings estão balanceadas.

Exercício 8:

Criei a variável contador = 0 para armazenar o número de ocorrências em que o padrão é encontrado.

Utilizei um ciclo for com range(len(s2) - len(s1) + 1). Este cálculo do limite superior é fundamental para garantir que o programa não tente ler para além do fim da string principal ao comparar os caracteres.

Dentro do ciclo, extraio uma slice de s2 que começa no índice atual i e tem o mesmo comprimento que s1.

-> Se essa slice (s2[i:i+len(s1)]) for exatamente igual a s1, significa que encontrámos o padrão e incrementamos o contador.

A função devolve o total acumulado, sendo capaz de identificar padrões.

Exercício 9:

Como as strings em Python não permitem a alteração da ordem dos seus caracteres diretamente, criei duas listas vazias (lista1 e lista2). Utilizei ciclos for para percorrer cada string e adicionar cada letra à sua respetiva lista.

Utilizei o método .sort() em ambas as listas. Este método organiza os caracteres por ordem alfabética. Se as palavras forem anagramas, as listas ordenadas ficarão idênticas.

Utilizei uma condição if/else para comparar as duas listas.

-> Se forem iguais, a função retorna True, confirmando o anagrama (ex: "listen" e "silent" tornam-se ambos ['e', 'i', 'l', 'n', 's', 't']).

-> Caso contrário, retorna False.



