# Funções criadas

def converte_data(dados):
    import datetime as dt
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
    # Verifica se a data de cada linha não está vazia e transforma para o formato brasileiro
    for linha in dados:
          for coluna in colunas_data:
              if linha[coluna] not in (None, ''):
                  linha[coluna] = dt.datetime.strptime(
                      linha[coluna],
                      '%Y-%m-%d %H:%M:%S'
                      ).strftime('%d-%m-%Y') # Transforma para o formato usado no Brasil conforme 
              else:
                  linha[coluna] = None # Se estiver vazia, atribui None
    print('- Data convertida para o formato usado no Brasil (%d-%m-%Y).')


def limpa_texto(dados):
  import re
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


def limpar_dados_faltantes(dados):
  import re
  print('=============== Dados originais (sem processamento) ===============\n')
  print('Nome do dataset: olist_products_dataset\n')
  print(f'Originalmente, os dados possuem {len(dados)} linhas\n')
  print('========================================\n')
  print('Quantidade de NAs por variável:\n')

  conta_nas = {}
  variaveis_para_remover = []
  dados_limpos = []

  # Conta a quantidade de NAs em cada uma das variáveis
  for linha in dados:
    for variavel in linha:
      if linha[variavel] is None or linha[variavel] == '':
        conta_nas[variavel] = conta_nas.get(variavel, 0) + 1

  # Esse trechinho só printa
  for var in conta_nas:
    if var == 'product_category_name':
      print(f'product_category_name: {conta_nas[var]} NAs.')
    else:
      print(f'{var}: {conta_nas[var]} NAs.')
  print('\n========================================\n')

  print('Porcentagem de NAs:\n')

  # Calcula a porcentagem de NAs para usar como critério para remoção
  for var in conta_nas:
    percentual = conta_nas[var]/len(dados)*100
    if conta_nas[var] > 0:
      print(f'{var}: {percentual:.5f}% de NAs.')
    if conta_nas[var] == 0:
      print(f'{var}: Não há NAs.')
    if percentual <= 1: # Inclui variáveis com quantidade de NAs igual ou menor que 1%
      variaveis_para_remover.append(var) # Inclui essas variáveis em um objeto

  # Inicia a remoção
  for linha in dados:
    remover = False
    # Se a variável estiver na lista para remoção e possuir NA, remove
    for var in variaveis_para_remover:
      if linha[var] is None or linha[var] == '':
        remover = True
    # Se não estiver na lista, inclui nos dados_limpos
    if not remover:
      dados_limpos.append(linha)

  # Preenchimento de valores com NAs ou ausentes

  """
  Regra imposta para product_category_name: "deve ser preenchido com a string
  'sem categoria'". Eu estendi esta regra para outras variáveis não numéricas
  """

  strings_prod = [
      'product_category_name',
      'product_name_lenght',
      'product_description_lenght',
      'product_photos_qty'
  ]
  padrao = r'_(.*?)_' # pega a palavrinha entre os underscores (_)

  for linha in dados_limpos:
    for var in linha:
      # Se a variável for string e se estiver nessa lista string_Prod
      if var in strings_prod and type(var) == str:
        # E se o valor for nulo ou inexistente
        if linha[var] is None or linha[var] == '':
          texto = var
          variavel = re.findall(padrao, texto)[0] # Eu coloquei o '[0]' porque retorna uma lista e nao uma string
          # Preencha com sem_ e o texto que eu peguei no meio do nome da variável
          preenchimento = "sem_" + variavel
          linha[var] = preenchimento

  print('\n========================================\n')
  print(f'Número inicial de linhas: {len(dados)} linhas')
  print('========================================\n')
  print(f'Foi realizado o preenchimento de {conta_nas['product_category_name']} valores inexistentes.')
  print(f'\nForam removidas {len(dados)-len(dados_limpos)} linhas após o processamento')
  print(f'\nNúmero final de linhas: {len(dados_limpos)} linhas')
  print('\n========================================\n')


    
