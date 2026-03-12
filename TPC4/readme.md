# TPC4: SKINTEA - A Arte do Cuidado da Pele

## Sobre o Projeto
O projeto **SKINTEA** foi desenvolvido no âmbito do TPC4 da unidade curricular de Processamento de Linguagem Natural (PLN). O objetivo deste trabalho consistiu na criação de uma página web sobre um tema à nossa escolha, aplicando conhecimentos práticos de desenvolvimento web front-end.

O tema selecionado foi "Skincare" (cuidados com a pele). A página funciona como um guia de aconselhamento digital, estruturado para educar o utilizador sobre a importância de uma rotina de cuidados, apresentar um enquadramento histórico da evolução da cosmética e, de forma interativa, fornecer protocolos de tratamento detalhados. Estes protocolos estão divididos por tipo de pele (Oleosa, Mista e Seca) e segmentados em rotinas de dia e de noite, com recomendações de produtos específicos para cada passo.

O design foi intencionalmente concebido para simular a estética de marcas de cosmética de segmento premium, priorizando o minimalismo, a legibilidade e a fluidez de navegação.

## Tecnologias e Arquitetura
A aplicação foi desenvolvida seguindo o conceito de *Single Page Application* (SPA), integrando estrutura, estilo e lógica num único ficheiro, dispensando o uso de bibliotecas ou frameworks externas.

* **HTML5:** Utilização de marcação semântica (como `<nav>`, `<section>`, `<header>`, `<footer>`) para garantir uma estrutura de documento acessível e bem organizada.
* **CSS3:** Estilização avançada para criar uma interface moderna e responsiva. Destaque para:
  * **Variáveis CSS (`:root`):** Implementação de uma paleta de cores consistente (tons pastel e terra).
  * **Flexbox e CSS Grid:** Utilizados para o alinhamento complexo de elementos, construção de grelhas de produtos responsivas e resolução de problemas de alinhamento vertical nos cartões de informação.
  * **Glassmorphism:** Aplicação de propriedades como `backdrop-filter: blur()` para criar efeitos de transparência e profundidade na barra de navegação e nos fundos dos cartões.
* **JavaScript (Vanilla):** Responsável pela interatividade da página, manipulação do Document Object Model (DOM) e controlo de animações baseadas no comportamento do utilizador.

## Funcionalidades e Implementação Técnica

### 1. Sistema Dinâmico de Navegação (Tabs e Sub-Tabs)
Para evitar o carregamento de múltiplas páginas e manter a fluidez, foi desenvolvido um sistema de abas duplas em JavaScript:
* **Nível Principal (Tipos de Pele):** O script oculta todos os blocos de conteúdo e apresenta apenas aquele que corresponde ao botão selecionado (Oleosa, Mista ou Seca).
* **Nível Secundário (Rotina de Dia/Noite):** Dentro de cada tipo de pele ativo, um segundo script gere a alternância entre os passos da manhã e da noite. A lógica foi desenhada para que, ao mudar de tipo de pele, a sub-aba "Rotina de Dia" seja reposta como visualização padrão.

### 2. Animações Baseadas em Scroll (Intersection Observer API)
Em vez de utilizar detetores de eventos de *scroll* tradicionais (que consomem muitos recursos do navegador), foi implementada a API `IntersectionObserver`. 
Este mecanismo monitoriza de forma assíncrona o momento em que os elementos HTML (marcados com a classe `.reveal`) entram no campo de visão do utilizador. Quando isso acontece, a classe `.active` é injetada, disparando uma transição CSS que faz os elementos aparecerem de forma suave (fade-in e translação vertical). O observador é em seguida desligado para esse elemento, otimizando o desempenho da página.

### 3. Soluções de Layout Específicas: O "Double Cleansing"
Um dos desafios técnicos consistiu em apresentar o passo de "Dupla Limpeza" (rotina de noite), que exige a exibição de dois produtos distintos lado a lado, acompanhados de texto descritivo, mantendo o alinhamento com os restantes cartões de produto único.
A solução passou pela criação de um contentor flexível dedicado (`.product-img-double`) e pela aplicação da propriedade `align-items: stretch` no cartão principal. Isto forçou as colunas de imagem e de texto a partilharem a mesma altura geométrica, permitindo um alinhamento perfeito ao centro, independentemente das proporções originais dos ficheiros de imagem (que foram normalizados com `object-fit: contain`).

## Estrutura do Diretório
O projeto está organizado da seguinte forma para facilitar a portabilidade:

```text
/TPC4
│
├── skincare.html       # Ficheiro principal contendo HTML, CSS e JavaScript
│
└── /imagens            # Diretório contendo todos os assets visuais locais
    ├── anua.jpg
    ├── barreiracutanea.png
    ├── cerave.jpg
    └── ... (restantes imagens referenciadas no código)