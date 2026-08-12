# Funções criadas

def converte_data(dados):

    """
    Esta função converte a data no formato de string para datetime. Após isso, muda
    o formato da data para o formato usado no brasil ('%d-%m-%Y') e volta a ser uma 
    string.
    """

    # Pega as colunas que possuem datas
    colunas_data = [
          'order_purchase_timestamp',
          'order_approved_at',
          'order_delivered_carrier_date',
          'order_delivered_customer_date',
          'order_estimated_delivery_date'
      ]

    for linha in dados:
          for coluna in colunas_data:
              if linha[coluna] not in (None, ''): # Verifica se a data não está vazia
                  linha[coluna] = dt.datetime.strptime(
                      linha[coluna],
                      '%Y-%m-%d %H:%M:%S'
                      ).strftime('%d-%m-%Y') # Transforma para o formato usado no Brasil conforme 
              else:
                  linha[coluna] = None # Se estiver vazia, atribui None
    print('- Data convertida para o formato usado no Brasil (%d-%m-%Y).')


def limpa_texto(dados):
  """
  Esta função limpa o nome da categoria dos produtos em cada linha, ou seja, transforma todas as letras
  em minúsculas, remove espaços nas extremidades do texto e substitui caracteres especiais e o
  underscore por ' '.

  Recebe um argumento (dados) que é uma lista de dicionários. Além disso, é obrigatório que df tenha uma chave
  chamada 'product_category_name'.
  """
  for linha in dados:
      texto = linha['product_category_name']
      # Verifica se não tem alguma linha sem informaçao
      if texto is not None:
          texto = texto.strip().lower() # Remove espaços em braco nas extremidades e transforma tudo para letra minúscula
      # Removi caracteres não alfa-numéricos e o underscore
      padrao = r'[^\w\s]+|_'
      # Substitui os caracteres do 'padrao' e substitui por ' '
      texto = re.sub(padrao, ' ', texto)
      
      linha['product_category_name'] = texto
  print('\n- Espaços desnecessários removidos.')
  print('- Caracteres não alfa-numéricos e o underscore removidos.\n')

def situacao_data_entrega(dados):
  print('=====================================================================')
  print('==================== SITUAÇÃO DA DATA DE ENTREGA ====================')
  print('=====================================================================')

  contagem = {}
  total_linhas = 0

  for linha in dados:

    total_linhas += 1
    # Cria uma coluna indicando a situação da data de entrega
    if linha['order_status'] == 'delivered' and linha['order_delivered_customer_date'] is None:
      linha['situacao_data_entrega'] = 'Falta data de entrega'
      print(f'-> Order_id {linha['order_id']} com falta de data de entrega!')
    if linha['order_status'] != 'delivered' and linha['order_delivered_customer_date'] is None:
      linha['situacao_data_entrega'] = 'OK! Sem data porque não foi entregue'
    elif linha['order_status'] != 'delivered' and linha['order_delivered_customer_date'] is not None:
      linha['situacao_data_entrega'] = 'Pedido não entregue com data'
      print(f'-> Order_id {linha['order_id']} com data de entrega mas que não foi entregue!')
    elif linha['order_status'] == 'delivered' and linha['order_delivered_customer_date'] is not None:
      linha['situacao_data_entrega'] = 'OK'
    
    situacao = linha['situacao_data_entrega']

    if situacao not in contagem:
      contagem[situacao] = 1
    else:
      contagem[situacao] += 1
    
  for categoria in contagem:
    if categoria == 'OK':
      print(f'\n- {contagem[categoria]} pedidos constam como OK')
    else:
      print(f'- {contagem[categoria]} pedidos constam como {categoria}')
  print('=======================================================================')



