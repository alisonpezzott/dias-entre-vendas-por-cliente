import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import random

# Parâmetros
num_clientes = 1000000
num_linhas = 10000000
path = "./vendas.csv"

# Gera os IDs de clientes
clientes = np.arange(1, num_clientes + 1)

# Função para gerar datas de venda
def gerar_datas_venda(num_meses):
    datas = []
    for _ in range(num_meses):
        datas.append((datetime.now() - timedelta(days=random.randint(0, 1830))).date())
    return datas

# Gera DataFrame
data = {
    'Cliente_ID': np.random.choice(clientes, num_linhas),
    'Valor': np.round(np.random.uniform(5000, 50000, num_linhas), 2),
    'Data': np.random.choice([date for cliente in clientes for date in gerar_datas_venda(random.randint(1, 12))], num_linhas)
}

df = pd.DataFrame(data)

# Ordena pela coluna de data
df = df.sort_values(by='Data')

# Adiciona sequencial do ID da venda
df['Venda_ID'] = np.arange(1, num_linhas + 1)

# Reorganiza as colunas
df = df[['Venda_ID','Data', 'Cliente_ID', 'Valor' ]]

# Salva em CSV
df.to_csv(path, index=False, sep=';')

print(f"DataFrame salvo em {path}")
