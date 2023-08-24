##Passo a passo##


import pandas as pd

# Ler as duas bases de dados
dados_empresas = pd.read_csv('dados_empresas.csv')
dados_ibov = pd.read_csv('ibov.csv')

# Filtrar as empresas que possuem liquidez acima de 1 MI

dados_empresas = dados_empresas[dados_empresas['volume_negociado']>1000000]

# Criar e calcular a coluna de rentabiliade mensal

dados_empresas['rentabilidade'] = dados_empresas.groupby('ticker')['preco_fechamento_ajustado'].pct_change()
dados_empresas['rentabilidade'] = dados_empresas.groupby('ticker')['rentabilidade'].shift(-1)

# Filtrar as empresas por rank de indicadores

dados_empresas['ranking_ebit_ev'] = dados_empresas.groupby('data')['ebit_ev'].rank(ascending = False)
dados_empresas['ranking_roic'] = dados_empresas.groupby('data')['roic'].rank(ascending = False)
dados_empresas['ranking_final'] = dados_empresas['ranking_ebit_ev'] + dados_empresas['ranking_roic']
dados_empresas['ranking_final'] = dados_empresas.groupby('data')['ranking_final'].rank()
# Filtrar que estão no top 10 de melhores indicadores em X período
dados_empresas[dados_empresas['data']== '2016-01-31']
dados_empresas = dados_empresas[dados_empresas['ranking_final']<=10]


# Calcular a rentabilidade da carteira
rentabilidade_carteira = dados_empresas.groupby('data')['rentabilidade'].mean()
rentabilidade_carteira = rentabilidade_carteira.to_frame()

# Calcular rentabiliade do modelo
rentabilidade_carteira['modelo'] = (1+ rentabilidade_carteira['rentabilidade']).cumprod()-1
rentabilidade_carteira = rentabilidade_carteira.shift(1)
rentabilidade_carteira = rentabilidade_carteira.dropna()
rentabilidade_carteira = rentabilidade_carteira.drop('rentabilidade', axis = 1)

# Trazer a rentabilidade do ínidce Bovespa para comparar com a rentabilidade do modelo
ibovespa = pd.read_csv('ibov.csv')
retorno_ibovespa = ibovespa['fechamento'].pct_change().dropna()
retorno_ibovespa_acum = (1 + retorno_ibovespa).cumprod() - 1
rentabilidade_carteira['ibovespa'] = retorno_ibovespa_acum.values
print(rentabilidade_carteira)