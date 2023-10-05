import requests
from bs4 import BeautifulSoup
import pandas as pd
import datetime

# Preencher variáveis de data para baixar corretamente o csv do Fundo Constellation com os dados
data_de_hoje = datetime.date.today()
ano = data_de_hoje.year
mes = data_de_hoje.month
mes_formatado = f"{mes:02d}"
dia_atual = data_de_hoje.day
dia = dia_atual - 1

# URL do arquivo CSV do Fundo Constellation
url1 = 'https://constellation.com.br/wp-content/uploads/{}/{}/Tabela-Site-{}-{}-{}.csv'.format(ano, mes_formatado, dia, mes_formatado, ano)

# Lista de URLs dos fundos de investimento
lista_de_urls = ['https://www.dynamo.com.br/pt', 'https://www.nucleocapital.com.br/']

# Extrair dados Dynamo e Nucleo
# Cria uma lista para armazenar os DataFrames individuais
dataframes = []

for url in lista_de_urls:
    # Faz uma solicitação HTTP para a página da web
    response = requests.get(url)

    # Verifica se a solicitação foi bem sucedida
    if response.status_code == 200:
        # Lê o conteúdo da página com BeautifulSoup
        soup = BeautifulSoup(response.text, 'html.parser')

        # Encontra todas as tabelas no HTML
        tables = soup.find_all('table')

        # Usa Pandas para ler a tabela HTML e criar um DataFrame
        df = pd.read_html(str(tables))[0]

        # Mantém apenas a primeira linha além do cabeçalho
        df = df.iloc[:2]

        # Reseta os índices do DataFrame
        df.reset_index(drop=True, inplace=True)

        # Adiciona o DataFrame à lista de DataFrames
        dataframes.append(df)
    else:
        print(f'Falha ao recuperar a página {url}. Código de status: {response.status_code}')

# Baixar csv com os dados do Fundo Constellation

# Faz o download do arquivo CSV
response = requests.get(url1)

# Verifica se o download foi bem-sucedido
if response.status_code == 200:
    # Salva o conteúdo do arquivo em um arquivo local
    with open('Base_Constellation.csv', 'wb') as file:
        file.write(response.content)

    # Lê o arquivo CSV com o Pandas
    df = pd.read_csv('Base_Constellation.csv', sep = ";")

    # Reseta índices do DataFrame
    df.reset_index(drop=True, inplace=True)

    # Mantém apenas as colunas utilizadas do data frame
    df=df[['Fundo','Dia','Ano']]
    # Mantém a linha apenas do fundo Constellation Ações FIC FIA
    df = df.iloc[0:1]

    # Adicione o DataFrame à lista de DataFrames
    dataframes.append(df)
    # Mensagem caso dê erro no download do csv
else:
    print(f'Falha ao baixar o arquivo. Código de status: {response.status_code}')



# Concatena os DataFrames individuais em um único DataFrame
df_final = pd.concat(dataframes, ignore_index=True)

# Limpa e coloca o data frame no padrão
df_final['Fundo *'] = df_final['Fundo *'].str.replace(r'\bInício.*', '', regex=True)
df_final = df_final[df_final['Fundo *'] != 'Dynamo Global FIC ']
df_final = df_final[['Fundo *','Dia','Ano']]
df_final.rename(columns={'Fundo *' : 'Fundo'}, inplace=True)
df_final['Gestora'] = ['Dynamo', 'Núcleo','Constellation','']
df_final = df_final[['Gestora', 'Fundo','Dia','Ano' ]]
df_final.loc[2, 'Fundo'] = 'Núcleo Ações FIC FIA'
df_final.loc[3, 'Fundo'] = 'Constellation FIC FIA'
df_final.loc[3,['Dia', 'Ano']]= df_final.loc[4,['Dia', 'Ano']] 
df_final = df_final.drop(4)
df_final= df_final.rename(columns={'Dia': 'Rentabilidade_Dia', 'Ano': 'Rentabiliade_Ano'})
colunas_valores = ['Rentabilidade_Dia','Rentabiliade_Ano']
df_final[colunas_valores] = df_final[colunas_valores].apply(lambda x: x.str.replace('.', ','))

# Converte o data frame pra um arquivo xlsx e armazena no mesmo local onde está o código
df_final.to_excel('Tabela_Rentabilidade_Fundos_Dados_site.xlsx', index = False, sheet_name = 'Resumo')

# Exibir mensagem de conclusão do código
print("A base, com os últimos dados da rentabilidade do ano e do dia dos fundos disponibilizados pelos sites da gestora, foi gerada com sucesso.")
