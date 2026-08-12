import csv
import re
import datetime as dt
#import kagglehub

# Funções criadas para esta tarefa
import mar as mo

# Download latest version
#path = kagglehub.dataset_download("olistbr/brazilian-ecommerce")
#print("Path to dataset files:", path)

#with open(path + '/olist_orders_dataset.csv',
with open('/olist_orders_dataset.csv',
          mode = 'r',
          encoding='utf-8') as arquivo:
    dados = list(csv.DictReader(arquivo))

with open('/olist_products_dataset.csv',
          mode = 'r',
          encoding='utf-8') as arquivo:
    dados_prod = list(csv.DictReader(arquivo))


mo.converte_data(dados)
mo.situacao_data_entrega(dados)
mo.limpa_texto(dados_prod)
mo.limpar_dados_faltantes(dados_prod)
