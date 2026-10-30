import pandas as pd
import matplotlib.pyplot as plt

# Ler o CSV
df = pd.read_csv("pedidos_prontos.csv")

# Converter a coluna de data
df["data"] = pd.to_datetime(df["data"])

# 1) Gráfico de linha: quantidade de pedidos por mês
pedidos_mes = df.groupby(df["data"].dt.to_period("M")).size()

plt.figure(figsize=(8,4))
pedidos_mes.plot(marker="o")
plt.title("Quantidade de Pedidos por Mês")
plt.xlabel("Mês")
plt.ylabel("Quantidade de Pedidos")
plt.grid(True)
plt.show()

# 2) Gráfico de barras: faturamento por canal
faturamento_canal = df.groupby("canal")["total"].sum()

plt.figure(figsize=(8,4))
faturamento_canal.plot(kind="bar")
plt.title("Faturamento por Canal")
plt.xlabel("Canal")
plt.ylabel("Faturamento")

plt.savefig("canal.png")

plt.show()

# 3) Gráfico de dispersão: preço x quantidade
plt.figure(figsize=(8,4))
plt.scatter(df["preco"], df["qtd"])
plt.title("Preço x Quantidade")
plt.xlabel("Preço")
plt.ylabel("Quantidade")
plt.grid(True)
plt.show()

print("""
Comentário:
No gráfico de dispersão, a maior parte dos pedidos possui
quantidade baixa (entre 1 e 4 unidades). Existem alguns
valores extremos com quantidade 40, que aparecem como outliers.
Não é possível observar uma relação forte entre preço e
quantidade comprada.
""")