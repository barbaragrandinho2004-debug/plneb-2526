## TPC8

## Descrição Geral

A aplicação foi desenvolvida em Python utilizando a micro-framework Flask para a gestão do backend e do roteamento. A interface de utilizador foi desenhada com foco na usabilidade, apresentando um design moderno e limpo, suportado por HTML5, CSS3 (com recurso a Bootstrap 5) e JavaScript. Os dados estão persistidos de forma local através de um ficheiro JSON, garantindo a integridade e atualização em tempo real das informações.

## Funcionalidades Principais

* **Pesquisa Avançada de Conceitos:**
  * Motor de busca capaz de analisar ocorrências tanto na designação (termo) como na descrição.
  * **Filtro Case Sensitive:** Opção para distinção estrita entre caracteres maiúsculos e minúsculos durante a pesquisa.
  * **Filtro de Palavra Exata (Word Boundary):** Restrição da pesquisa a palavras isoladas, evitando falsos positivos em substrings.
  * Destaque visual e formatação dinâmica (negrito) dos termos encontrados nos resultados da pesquisa.
* **Gestão de Terminologia (CRUD):**
  * Listagem alfabética de todos os conceitos médicos disponíveis na base de dados.
  * Consulta detalhada da descrição de cada termo.
  * Inserção de novos conceitos através de formulário validado.
  * Eliminação de conceitos desatualizados ou incorretos (processado via chamadas assíncronas AJAX).
* **Apresentação em Tabela Dinâmica:**
  * Visualização integrada dos dados numa tabela interativa utilizando a biblioteca DataTables.
  * Suporte nativo para paginação, ordenação alfabética e filtragem rápida.

## Arquitetura e Tecnologias

* **Backend:** Python 3.x, Flask.
* **Frontend:** HTML5, CSS3, Jinja2 (Motor de Templates).
* **Bibliotecas Client-Side:** jQuery, Bootstrap 5, DataTables.
* **Persistência de Dados:** JSON (JavaScript Object Notation).

## Estrutura do Diretório

* `aula7_2.py`: Módulo principal do servidor contendo as rotas e a lógica de processamento textual.
* `bd.json` / `dicionario_medico.json`: Ficheiro de base de dados contendo o dicionário (chave-valor).
* `templates/`:
  * `layout.html`: Template base com as dependências e a barra de navegação principal.
  * `home.html`: Página inicial com a apresentação da plataforma e métricas.
  * `conceitos.html`: Interface para listagem e formulário de adição de novos termos.
  * `conceito.html`: Interface para visualização de detalhes e opção de remoção.
  * `pesquisar.html`: Interface do motor de busca e apresentação de resultados.
  * `tabela.html`: Visualização global através de DataTables.
* `static/script/script.js`: Lógica JavaScript para manipulação do DOM e requisições assíncronas (ex: método DELETE).

## Instruções de Execução

1. Certifique-se de que possui o Python 3 instalado no seu ambiente.
2. Instale as dependências necessárias, nomeadamente a framework Flask:
    ```bash
    pip install Flask
    ```
3. Na raiz do projeto, inicie o servidor local:
    ```bash
    python aula7_2.py
    ```
4. Aceda à aplicação através do navegador web utilizando o endereço:
    ```text
    http://localhost:4002
    ```