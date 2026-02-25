Exercício 1 (Alíneas 1.1 a 1.5):
Utilizei as funções base da biblioteca re para diferentes níveis de pesquisa:

Alínea 1.1: Recorri a re.match() com o âncoras ^ para garantir que a palavra "hello" fosse procurada apenas no início da linha.

Alínea 1.2: Utilizei re.search() para encontrar a palavra em qualquer posição da string, retornando um valor booleano.

Alínea 1.3: Apliquei re.findall() em conjunto com a flag re.IGNORECASE para extrair todas as instâncias de "hello" independentemente de serem maiúsculas ou minúsculas.

Alínea 1.4: Usei re.sub() para substituir todas as ocorrências de "hello" por "YEP", recorrendo ao prefixo (?i) dentro da expressão regular para ignorar a capitalização.

Alínea 1.5: Utilizei o re.split() com o padrão r",\s*" para dividir a string em cada vírgula, tratando automaticamente possíveis espaços extra após a mesma.

Exercício 2:
Defini a função palavra_magica utilizando re.search(). A expressão regular r"por favor[.,;?!]+$" foi desenhada para verificar se a frase termina com "por favor" seguido obrigatoriamente de um ou mais sinais de pontuação válidos, utilizando a âncora $ para marcar o fim da linha.

Exercício 3:
Na função narcissismo, utilizei o re.findall() com o padrão r"\beu\b". O uso de \b (word boundaries) é crucial aqui para garantir que a função conte apenas a palavra "eu" isolada e não a encontre dentro de outras palavras como "meu" ou "judeu".

Exercício 4:
Para a função troca_de_curso, utilizei o método re.sub(). Este método recebe o padrão fixo "LEI" e substitui-o pela variável novo_curso passada como argumento, permitindo uma atualização dinâmica do texto fornecido.

Exercício 5:
Na função soma_string, combinei o re.split(r",", linha) para transformar a string numa lista de substrings numéricas. Depois, utilizei uma list comprehension para converter cada elemento em inteiro (int(n)) e apliquei a função sum() para obter o total.

Exercício 6:
Criei a função pronomes recorrendo a um grupo de captura com o operador de união | (ex: eu|tu|ele|...). Utilizei novamente as \b para evitar correspondências parciais e a flag re.IGNORECASE para capturar pronomes tanto no início como no meio das frases.

Exercício 7:
Para validar nomes de variáveis em variavel_valida, utilizei re.match() com o padrão r"^[a-zA-Z][a-zA-Z0-9_]*$".

^[a-zA-Z] garante que o primeiro caracter é obrigatoriamente uma letra.

[a-zA-Z0-9_]*$ permite que o resto da string contenha letras, números ou underscores até ao seu final.

Exercício 8:
Na função inteiros, utilizei re.findall(r"-?\d+", texto). O padrão -? indica que o sinal de menos é opcional (0 ou 1 ocorrência), e \d+ captura um ou mais dígitos consecutivos, permitindo identificar números positivos e negativos.

Exercício 9:
Para a função underscores, utilizei re.sub() com o padrão r" +". O sinal + é fundamental pois identifica um ou mais espaços seguidos, permitindo que múltiplos espaços em branco sejam condensados e substituídos por um único caracter de underscore.

Exercício 10:
Na função codigos_postais, utilizei um ciclo for para percorrer a lista de códigos. Dentro do ciclo, apliquei re.split(r"-", cp) para separar as duas partes do código postal e converti o resultado num tuple(), adicionando-o a uma lista final de pares.