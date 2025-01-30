import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import random

# Configurações
num_clientes = 50000
num_lojas = 10
num_linhas = 2000000

# Gerar IDs de clientes e lojas
clientes = np.arange(1, num_clientes + 1)
lojas = np.arange(1, num_lojas + 1)

# Função para gerar datas de venda
def gerar_datas_venda(num_meses):
    datas = []
    for _ in range(num_meses):
        datas.append((datetime.now() - timedelta(days=random.randint(0, 4000))).date())
    return datas

# Gerar DataFrame
data = {
    'Cliente_ID': np.random.choice(clientes, num_linhas),
    'Loja_ID': np.random.choice(lojas, num_linhas),
    'Valor': np.round(np.random.uniform(200.0, 5000.0, num_linhas), 2),
    'Data': np.random.choice([date for cliente in clientes for date in gerar_datas_venda(random.randint(1, 12))], num_linhas)
}

df = pd.DataFrame(data)

# Ordenar DataFrame pela coluna de data
df = df.sort_values(by='Data')

# Adicionar coluna de ID de venda sequencial
df['Venda_ID'] = np.arange(1, num_linhas + 1)

# Reorganizar colunas para que Venda_ID seja a primeira
df = df[['Venda_ID', 'Data', 'Cliente_ID', 'Loja_ID', 'Valor' ]]

# Salvar em arquivo CSV
df.to_csv('vendas.csv', index=False, sep=';')

print("DataFrame salvo em vendas.csv")