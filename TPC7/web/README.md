# Dicionário Médico Online

Este projeto é uma aplicação web desenvolvida em Python (Flask) para visualização e pesquisa de conceitos médicos. Foi desenvolvido no âmbito da Unidade Curricular de Processamento de Linguagem Natural (PLN).

A interface foi desenhada com foco em tons pastel, oferecendo uma experiência de utilização limpa e esteticamente agradável.

## Funcionalidades

* **Página Inicial:** Apresentação com contagem dinâmica do número total de conceitos médicos disponíveis no dicionário.
* **Lista de Conceitos:** Visualização completa e interativa de todos os termos médicos alfabeticamente.
* **Detalhe do Conceito:** Página individual para cada termo, exibindo a sua designação e respetiva descrição detalhada.
* **API de Dados:** Endpoint (`/api/conceitos`) que retorna o dicionário completo em formato JSON bruto.

## Tecnologias Utilizadas

* **Backend:** Python 3, Flask
* **Frontend:** HTML5, CSS3, Jinja2 (Templates)
* **Tipografia:** Google Fonts (Nunito)

## Requisitos do Projeto

Para que o projeto funcione corretamente na tua máquina, precisas de garantir os seguintes requisitos:

### Requisitos de Software (Ambiente)
* **Python 3.x:** A versão base da linguagem necessária para correr a aplicação.
* **Navegador Web:** Qualquer navegador atual (Chrome, Firefox, Edge, Safari) para visualizar a interface.
* **Ligação à Internet:** Necessária apenas no lado do cliente (navegador) para carregar a fonte "Nunito" a partir do Google Fonts.

### Requisitos de Bibliotecas (Dependências Python)
* **Flask:** A framework web utilizada. Pode ser instalada via terminal com o comando:
  `pip install Flask`

*(Nota: A biblioteca `json` utilizada no código é nativa do Python, logo não necessita de instalação adicional).*

### Requisitos de Dados
* **Ficheiro JSON:** O ficheiro `dicionario_medico.json` tem de existir e estar acessível. O caminho para este ficheiro deve estar corretamente configurado na função `open()` dentro do script `aula7_web.py`.

## Estrutura do Projeto

Para que o Flask encontre as páginas HTML, a estrutura de pastas tem de ser rigorosamente esta:

```text
AULA7/
│
├── aula7_web.py               # Script principal da aplicação Flask
├── dicionario_medico.json     # Base de dados (verifica o caminho no código)
│
└── templates/                 # Pasta para os ficheiros HTML
    ├── layout.html            # Estrutura base da página
    ├── home.html              # Página Inicial
    ├── conceitos.html         # Lista de todos os termos
    ├── conceito.html          # Página de um termo específico