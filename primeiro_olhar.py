import pandas as pd

# ==========================
# LEITURA DOS ARQUIVOS
# ==========================

pedidos = pd.read_csv("pedidos.csv")
produtos = pd.read_csv("produtos.csv")

# ==========================
# MERGE
# ==========================

base = pedidos.merge(
    produtos,
    on="id_produto",
    how="left"
)

# ==========================
# SHAPE
# ==========================

print("=" * 50)
print("SHAPE")
print(base.shape)

# ==========================
# HEAD
# ==========================

print("\n" + "=" * 50)
print("HEAD")
print(base.head())

# ==========================
# INFO
# ==========================

print("\n" + "=" * 50)
print("INFO")
print(base.info())

# ==========================
# DESCRIBE
# ==========================

print("\n" + "=" * 50)
print("DESCRIBE")
print(base.describe(include="all"))

# ==========================
# NULOS
# ==========================

print("\n" + "=" * 50)
print("PROPORÇÃO DE NULOS (%)")

nulos = (
    base.isna()
    .mean()
    .mul(100)
    .round(2)
    .sort_values(ascending=False)
)

print(nulos)

# ==========================
# DUPLICADOS
# ==========================

print("\n" + "=" * 50)
print("DUPLICADOS")

duplicados = base.duplicated().sum()
print(duplicados)

# ==========================
# CANAIS DISTINTOS
# ==========================

print("\n" + "=" * 50)
print("VALORES DISTINTOS DE CANAL")

print(base["canal"].unique())

# ==========================
# OBSERVAÇÕES
# ==========================

"""
OBSERVAÇÃO 1:
Há muitos valores ausentes em id_cliente,
avaliacao e tempo_entrega_min.

OBSERVAÇÃO 2:
Existem registros duplicados que devem ser
investigados antes de qualquer análise.

OBSERVAÇÃO 3:
A coluna canal possui problemas de padronização
(APP, App, app, Delivery, delivery, Balcão, balcão),
sendo necessária uma limpeza dos dados.
"""