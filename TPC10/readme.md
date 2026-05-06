## TPC10

O projeto utiliza o modelo pré-treinado `bert-base-portuguese-cased` (da NeuralMind) e faz o *fine-tuning* (ajuste fino) através do dataset `lfcc/portuguese_ner` disponibilizado na Hugging Face.

O objetivo do modelo é identificar e classificar entidades num texto nas seguintes categorias:
* **Data** (Datas e períodos)
* **Local** (Cidades, países, localizações físicas)
* **Organização** (Empresas, instituições)
* **Pessoa** (Nomes próprios)
* **Profissão** (Cargos e ofícios)

---

## Tecnologias e Bibliotecas Utilizadas
* **Linguagem:** Python 3
* **Bibliotecas Principais:** * `transformers` (Pipelines, Tokenization e Trainer da Hugging Face)
  * `datasets` (Carregamento e manipulação de dados)
  * `evaluate` e `seqeval` (Cálculo de métricas de avaliação do modelo)
  * `PyTorch` (Backend de Machine Learning)

---

## Estrutura do Notebook

O notebook está organizado nas seguintes fases de desenvolvimento:

1. **Data Loading:** Instalação das dependências e carregamento do dataset `lfcc/portuguese_ner` (splits de treino e teste).
2. **Data Pre-Processing:** Carregamento do tokenizador BERT e alinhamento correto das *labels* (etiquetas) com os *tokens* gerados, garantindo que sub-palavras recebem a classificação `-100` para serem ignoradas no cálculo da *loss*.
3. **Model Training:** Configuração do `AutoModelForTokenClassification` e definição dos hiperparâmetros de treino (ex: learning rate, epochs, batch size) utilizando a classe `Trainer`.
4. **Evaluate:** Implementação da função `compute_metrics` utilizando a biblioteca `seqeval` para extrair resultados reais de Precisão, Recall, F1-Score e Exatidão (Accuracy).
5. **Inference:** Teste prático do modelo treinado através do `pipeline` de NER da Hugging Face, aplicando-o a textos novos não vistos durante o treino.

---

## Como Executar

1. Importar o notebook (`TPC10.ipynb`) para o Google Colab ou um ambiente Jupyter local.
2. Garantir que o ambiente tem acesso a um GPU (no Colab: `Runtime > Change runtime type > T4 GPU`) para acelerar o treino.
3. Executar as células sequencialmente. A primeira célula irá instalar automaticamente todas as dependências necessárias.
4. Na secção de **Inference**, é possível alterar a variável que contém o texto de input para testar a capacidade do modelo noutros cenários.