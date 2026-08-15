# Mini-Projeto Avaliativo - Módulo 1 - Semana 07

## Índice

- [Descrição do projeto](#descrição-do-projeto)
- [Estrutura do projeto](#estrutura-do-projeto)
- [Requisitos](#requisitos)
- [Como executar](#como-executar)
- [Etapas do pipeline](#etapas-do-pipeline)
  - [1. Tratamento de dados ausentes](#1-tratamento-de-dados-ausentes)
  - [2. Padronização de textos e Regex](#2-padronização-de-textos-e-regex)
  - [3. Validação das datas de entrega](#3-validação-das-datas-de-entrega)
  - [4. Conversão de datas](#4-conversão-de-datas)
- [Resultado esperado](#resultado-esperado)
- [Reflexão teórica: relação com Machine Learning](#reflexão-teórica-relação-com-machine-learning)
- [Tecnologias utilizadas](#tecnologias-utilizadas)
- [Autoria](#autoria)

## Descrição do projeto

Este projeto foi desenvolvido como atividade avaliativa da etapa [Carreira Tech - Trilha Inteligência Artificial
Fundamentos de Programação, Dados e Machine Learning do Programa SCTEC - SCTI executado pelo SENAI-SC](https://sctec.scti.sc.gov.br/) e tem como **objetivo** construir um pipeline de sanitização para os dados do e-commerce brasileiro da Olist.

A proposta parte de dois arquivos CSV extraídos da base oficial da Olist:

- `olist_products_dataset.csv`
- `olist_orders_dataset.csv`

O **objetivo do script** é identificar e tratar inconsistências que podem comprometer análises, relatórios e, posteriormente, modelos de Machine Learning. O projeto foi desenvolvido utilizando apenas bibliotecas nativas do Python, `csv`, `re` e `datetime`.

O arquivo [main.py](main.py) realiza o carregamento dos dois datasets e chama as funções desenvolvidas no módulo [mar.py](mar.py).

## Estrutura do projeto

```text
.
├── main.py
├── mar.py
├── olist_products_dataset.csv
├── olist_orders_dataset.csv
└── README.md
```

### `main.py`

[main.py](main.py) o script principal do projeto. Ele importa o módulo `mar`, lê os arquivos CSV com `csv.DictReader` e aplica as funções de tratamento aos dados carregados.

### `mar.py`

[mar.py](mar.py) contém as funções responsáveis pelas etapas de sanitização:

- `converte_data()`
- `situacao_data_entrega()`
- `limpa_texto()`
- `limpar_dados_faltantes()`

## Requisitos

- Python 3.x
- Os arquivos `olist_products_dataset.csv` e `olist_orders_dataset.csv`
- Nenhuma instalação de biblioteca externa é necessária para executar a versão atual do projeto.

## Como executar

### 1. Clone o repositório

```bash
git clone <https://github.com/Mauritia-flexuosa/miniprojeto.git>
cd miniprojeto
```

### 2. Coloque os arquivos CSV no diretório do projeto

Certifique-se de que os arquivos abaixo estejam disponíveis:

```text
olist_products_dataset.csv
olist_orders_dataset.csv
```

### 3. Verifique os caminhos dos arquivos

Durante o teste, eu tive uma surpresa: erro. No `main.py`, os arquivos eram abertos pelos caminhos:

```python
with open('/olist_orders_dataset.csv', mode='r', encoding='utf-8') as arquivo:
```

```python
with open('/olist_products_dataset.csv', mode='r', encoding='utf-8') as arquivo:
```

Como os CSVs estão na mesma pasta do projeto, precisei alterar para caminhos sem a barra (`/`):

```python
with open('olist_orders_dataset.csv', mode='r', encoding='utf-8') as arquivo:
```

```python
with open('olist_products_dataset.csv', mode='r', encoding='utf-8') as arquivo:
```

### 4. Execute o programa

No terminal:

```bash
python main.py
```

## Etapas do pipeline

### 1. Tratamento de dados ausentes

Ao explorar os dados, percebi que algumas variáveis apresentavam aproximadamente 0,006% de NAs. Então escolhi a opção mais parcimoniosa que era remover estas unidades amostrais.

A função `limpar_dados_faltantes()` percorre os registros do dataset de produtos, contabiliza valores `None` ou strings vazias e calcula a porcentagem de dados ausentes por variável.

Para criar um critério mais abrangente (pensando em adição de dados futuros), o código foi pensado para utilizarrum critério de corte para identificar variáveis com proporção de ausências menor que 1% e remover os registros que apresentam valores ausentes nessas variáveis.

``` python
  # Calcula a porcentagem de NAs para usar como critério para remoção
  for var in conta_nas:
    percentual = conta_nas[var]/len(dados)*100
    if conta_nas[var] > 0:
      print(f'{var}: {percentual:.5f}% de NAs.')
    if conta_nas[var] == 0:
      print(f'{var}: Não há NAs.')
    if percentual <= 1: # Inclui variáveis com quantidade de NAs igual ou menor que 1%
      variaveis_para_remover.append(var) # Inclui essas variáveis em um objeto
```

Para `product_category_name`, foi adotada uma regra específica de preenchimento dos valores ausentes imposta no desafio: `Sempre que encontrar um valor nulo/vazio na coluna product_category_name, ele deve ser preenchido com a string "sem categoria".`. O código também foi pensado para estender essa estratégia para outras variáveis tratadas como strings, gerando valores no padrão `sem_<categoria>`. Esta iniciativa foi tomada pelo entendimento de que, como são menos de 2% dos dados faltantes para esta variável, o critério poderia ser facilmente aplicado a variáveis de "importância" presumivelmente similares e com o mesmo número de ausências. 

### 2. Padronização de textos e Regex

A função `limpa_texto()` realiza a padronização de `product_category_name`, removendo espaços excedentes nas extremidades com `.strip()`, convertendo o texto para letras minúsculas com `.lower()` e utilizando uma expressão regular para remover caracteres não alfanuméricos e underscores.

### 3. Validação das datas de entrega

A função `situacao_data_entrega()` verifica a relação entre `order_status` e `order_delivered_customer_date`. Para cada pedido, é criada a variável `situacao_data_entrega`, classificando registros como `OK`, `Falta data de entrega`, `OK! Sem data porque não foi entregue` ou `Pedido não entregue com data`. O objetivo é verificar a hipótese de negócio de que pedidos sem data de entrega devem estar associados a pedidos que não foram entregues.

### 4. Conversão de datas

A função `converte_data()` identifica as colunas temporais do dataset de pedidos, converte as strings para objetos `datetime` utilizando o formato original `%Y-%m-%d %H:%M:%S` e, em seguida, formata as datas para `%d-%m-%Y`. Valores vazios são mantidos como `None`.

## Resultado esperado

Ao final da execução, o programa apresenta informações de controle sobre o processamento, incluindo a quantidade de linhas originais, a quantidade de valores ausentes identificados, o número de registros removidos e o número final de linhas após o tratamento dos dados. 

## Reflexão teórica: relação com Machine Learning

A qualidade dos dados utilizados para construção de modelos é fundamental para definir o desempenho e usabilidade destes modelos. Além do processo de coleta de dados ser fundamental para definir a qualidade dos dados, o tratamento de dados quase sempre é necessário por conter erros, inconsistências e diferentes formatos. Por exemplo, dados com texto não padronizado, ausentes, inconsistentes ou em formatos inadequados podem gerar ruido e falsos padrões no conjunto de treinamento. Isto pode enviesar os resultados e gerar um modelo que represente inadequadamente os padrões dos dados e que não tenha um bom desempenho com outro conjunto de dados.

Além disso, overfitting ocorre quando o modelo aprende excessivamente os padrões específicos dos dados de treinamento e perde a capacidade de generalização. Entretanto, o tratamento de dados não é suficiente para eliminar o overfitting. A separação adequada do treino e teste, validações do desempenho, escolha adequadaa de variáveis e definição da complexidade do modelo são necessários para evitar overfitting. Assim, a limpeza e sanitização dos dados são etapas fundamentais antes do treinamento de modelos de Machine Learning, contribuindo para a construção de modelos baseados em dados consistentes. 

## Tecnologias utilizadas

- Python 3
- `csv`
- `re`
- `datetime`
- Estruturas nativas da linguagem: listas, dicionários, laços `for`, condicionais `if/elif/else` e funções customizadas.

## Autoria

Projeto desenvolvido por *Marcio Baldissera Cure* como atividade avaliativa da etapa profissionalizar da Trilha de Inteligência artificial do Carreira Tech, do Programa SCTEC - SCTI/SESC.