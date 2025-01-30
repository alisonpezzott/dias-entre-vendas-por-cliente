import pandas as pd
import numpy as np
import pyarrow as pa
import pyarrow.parquet as pq
from datetime import datetime, timedelta
import random

# Configurações
num_clientes = 10000
num_lojas = 10
num_linhas = 2000000

# Gerar IDs de clientes e lojas
clientes = np.arange(1, num_clientes + 1)
lojas = np.arange(1, num_lojas + 1)

# Função para gerar datas de venda
def gerar_datas_venda(num_meses):
    datas = []
    for _ in range(num_meses):
        datas.append(datetime.now() - timedelta(days=random.randint(0, 365)))
    return datas

# Gerar DataFrame
data = {
    'Cliente_ID': np.random.choice(clientes, num_linhas),
    'Loja_ID': np.random.choice(lojas, num_linhas),
    'Valor': np.random.uniform(200.0, 5000.0, num_linhas),
    'Data': np.random.choice([date for cliente in clientes for date in gerar_datas_venda(random.randint(1, 12))], num_linhas)
}

df = pd.DataFrame(data)

# Salvar em arquivo Parquet
df.to_parquet('vendas.parquet', engine='pyarrow')

print("DataFrame salvo em vendas.parquet")