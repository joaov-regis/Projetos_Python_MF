import pandas as pd
import requests
import zipfile
import datetime
import io
import pyodbc
import openpyxl

# Setar a formatação padrão para os números
pd.options.display.float_format = '{:.2f}'.format

# Preencher variáveis para trazer os dados da CVM sobre os fundos
data_inicial = datetime.date(2023, 8, 1)
data_final = datetime.date(2023, 9, 1)
ano_atual = data_inicial.year
mes_atual = data_inicial.month
data_de_hoje = datetime.date.today()
dia_atual = data_de_hoje.day
dia = dia_atual - 1

anos = []  # Lista para armazenar os anos
meses = []  # Lista para armazenar os meses

# Cria uma lista de datas no formato "AAAA-MM" para iterar
datas = []

while (ano_atual, mes_atual) <= (data_final.year, data_final.month):
    ano_str = str(ano_atual)
    mes_str = f"{mes_atual:02d}"
    datas.append(f"{ano_str}-{mes_str}")
    
    anos.append(ano_str)
    meses.append(mes_str)
    
    if mes_atual == 12:
        ano_atual += 1
        mes_atual = 1
    else:
        mes_atual += 1

# Cria um DataFrame vazio para armazenar todos os dados
dados_fundos = pd.DataFrame()

# Loop através das datas baixa e concatena os dados de cada mês
for ano, mes in zip(anos, meses):
    url = f'https://dados.cvm.gov.br/dados/FI/DOC/INF_DIARIO/DADOS/inf_diario_fi_{ano}{mes}.zip'

    download = requests.get(url)

    with open(f"inf_diario_fi_{ano}{mes}.zip", "wb") as arquivo_cvm:
        arquivo_cvm.write(download.content)

    # Descompacta o arquivo ZIP manualmente
    with zipfile.ZipFile(f"inf_diario_fi_{ano}{mes}.zip", "r") as arquivo_zip:
        arquivo_zip.extractall()
    
    # Verifica se há arquivos no formato CSV antes de tentar lê-los
    arquivos_csv = [file for file in arquivo_zip.namelist() if file.lower().endswith('.csv')]
    
    if len(arquivos_csv) > 0:
        # Lê o primeiro arquivo CSV encontrado
        arquivo_csv = arquivos_csv[0]
        dados_mensais = pd.read_csv(arquivo_csv, sep=";", encoding='ISO-8859-1')

        # Concatena os dados mensais ao DataFrame principal
        dados_fundos = pd.concat([dados_fundos, dados_mensais], ignore_index=True)



# Lê os dados de cadastros dos fundos
dados_cadastro = pd.read_csv('cad_fi.csv', 
                             sep = ";", encoding = 'ISO-8859-1')

dados_cadastro = dados_cadastro[['CNPJ_FUNDO', 'DENOM_SOCIAL']]

# Elimina cadastros duplicados
dados_cadastro = dados_cadastro.drop_duplicates()

# Procura o CNPJ do fundo na planilha de cadastros e traz os valores referentes a ele
base_final = pd.merge(dados_fundos, dados_cadastro, how = "left",
                      left_on = ["CNPJ_FUNDO"], right_on = ["CNPJ_FUNDO"])

# Deixa somente as colunas do CNPJ, Nome do Fundo, Data e valor da cota no data frame
base_final = base_final[['CNPJ_FUNDO', 'DENOM_SOCIAL', 'DT_COMPTC', 'VL_QUOTA']]
base_final = pd.DataFrame(base_final)

# Salva a base de dados em excel
base_final.to_excel('Base_Dados_Cotas_Diarias_CVM.xlsx', engine='openpyxl', index=False)


# Caso queira passar a base para um arquivo Acess #
# OBS: Retirar # para rodar essa parte do código

# Suponha que você tenha um DataFrame chamado 'df' que deseja salvar no Access

# Configurar a conexão com o banco de dados Access
# conn_str = r'DRIVER={Microsoft Access Driver (*.mdb, *.accdb)};'  # Use o driver correto para sua versão do Access
# db_path = r'C:\caminho\para\seu\arquivo.accdb'  # Substitua pelo caminho para o seu arquivo Access
# conn = pyodbc.connect(conn_str + f'DBQ={db_path}')

# Converter o DataFrame em uma tabela Access
# table_name = 'NomeDaTabela'  # Substitua pelo nome da tabela que você deseja criar ou substituir
# base_final.to_sql(table_name, conn, if_exists='replace', index=False)

# Fechar a conexão com o banco de dados
# conn.close()

# print(f'DataFrame salvo com sucesso na tabela {table_name} do banco de dados Access.')
