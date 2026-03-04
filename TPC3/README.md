# TPC 3

## Objetivo
Este projeto tem como objetivo processar um ficheiro de texto contendo um dicionário médico (`dicionario_medico.txt`), extrair os seus conceitos e respetivas descrições, e exportar a informação estruturada para formatos mais acessíveis (JSON e HTML). 

O desafio principal (TPC3) consistiu em resolver o problema das quebras de página (caracteres de *form feed* `\f`), que dividiam descrições a meio das frases ou criavam falsos conceitos, prejudicando o algoritmo de extração base.

## Metodologia e Lógica de Resolução

Para limpar o texto de forma segura sem perder a estrutura original, utilizou-se uma estratégia de **marcação temporária** com Expressões Regulares (`re`):

1. **Substituição Inicial**: Substituição dos caracteres de *form feed* (`\f`) por quebras de linha normais (`\n`).
2. **Marcação (Andaime Temporário)**: Inserção de um marcador `@` após cada duplo enter (`\n\n`), assumindo inicialmente que estes representam a separação padrão entre conceitos.
3. **Correção de Frases Cortadas (Falsos Conceitos)**:
   - Regex: `r"([a-zà-úç])\s*\n\n@\n\s*([a-zà-úç])"`
   - **Lógica**: Se após a limpeza ocorrer o nosso marcador `@` ladeado por letras minúsculas (incluindo o "ç"), significa que a página quebrou a meio de uma descrição. O algoritmo remove o marcador e os *enters*, voltando a unir a frase.
4. **Correção de Quebras Pós-Definição**:
   - Regex: `r"\n\n@\n([A-ZÀ-ÚÇ])"`
   - **Lógica**: Ocorre quando o salto de página acontece imediatamente após o ponto final de uma descrição. Esta regex previne que a letra maiúscula do conceito seguinte fique isolada com marcações excessivas.
5. **Limpeza Final**:
   - Regex: `r"@"` -> `""`
   - **Lógica**: Após as correções estarem feitas, o marcador `@` já não é necessário. Removemos todos os `@`, deixando apenas os `\n\n` legítimos que separam os conceitos de forma correta e limpa.
6. **Extração e Estruturação**:
   - O texto limpo é guardado num novo ficheiro (`dicionario_medico_tratado.txt`).
   - O texto é dividido (`re.split(r"\n\n")`) usando os espaçamentos agora validados.
   - Cada bloco é novamente dividido (`maxsplit=1`) pelo primeiro `\n` para separar a "Designação" da "Descrição", populando um dicionário em Python.

## Ficheiros Gerados
A execução do script gera três ficheiros de output:
1. `dicionario_medico_tratado.txt`: O texto do dicionário completamente limpo e corrigido (sem quebras a meio e sem caracteres de marcação).
2. `dicionario_medico.json`: Ficheiro com a representação estruturada em JSON do dicionário.
3. `dicionario_medico.html`: Página web formatada para visualização rápida dos termos médicos no browser.