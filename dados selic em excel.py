import pandas as pd
import requests
import datetime as dt

# Define o intervalo de datas que os dados serão extraídos

data_inicio = '2000-01-01'
data_fim = '2023-08-19'


# URL do serviço de dados do Banco Central do Brasil para a Taxa Selic
url = "https://api.bcb.gov.br/dados/serie/bcdata.sgs.11/dados?formato=json"

# Faz a requisição GET para obter os dados em formato JSON
response = requests.get(url)

# Verifica se a requisição foi bem-sucedida
if response.status_code == 200:
    data = response.json()

    # Cria um DataFrame com os dados
    df = pd.DataFrame(data)

    # Converte a coluna "valor" para valores numéricos
    df['valor'] = df['valor'].str.replace(',', '.').astype(float)


    # Salva o relatório no excel
    df.to_excel('Selic.xlsx', index= False)
else:
    print("Erro ao obter os dados da Taxa Selic")
