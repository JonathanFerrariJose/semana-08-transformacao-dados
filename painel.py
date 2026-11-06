import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.ticker import FuncFormatter

# Ler CSV
df = pd.read_csv(
    "pedidos_prontos.csv",
    comment="<",
    on_bad_lines="skip"
)

# Garantir que total seja numérico
df["total"] = pd.to_numeric(df["total"], errors="coerce")

# Remover linhas inválidas
df = df.dropna(subset=["total"])

# =========================
# AGRUPAMENTOS
# =========================

fat_mes = df.groupby("mes")["total"].sum()

fat_categoria = (
    df.groupby("categoria")["total"]
    .sum()
    .sort_values(ascending=False)
)

fat_canal = (
    df.groupby("canal")["total"]
    .sum()
    .sort_values(ascending=False)
)

# =========================
# SUBPLOTS
# =========================

fig, axs = plt.subplots(2, 2, figsize=(14, 10))

# Gráfico 1 - Mês
axs[0, 0].plot(
    fat_mes.index,
    fat_mes.values,
    marker="o",
    color="steelblue"
)
axs[0, 0].set_title("Faturamento por Mês")
axs[0, 0].set_xlabel("Mês")
axs[0, 0].set_ylabel("R$")

# Gráfico 2 - Categoria
axs[0, 1].bar(
    fat_categoria.index,
    fat_categoria.values,
    color="seagreen"
)
axs[0, 1].set_title("Faturamento por Categoria")
axs[0, 1].tick_params(axis="x", rotation=30)

# Gráfico 3 - Canal
axs[1, 0].bar(
    fat_canal.index,
    fat_canal.values,
    color="orange"
)
axs[1, 0].set_title("Faturamento por Canal")

# Gráfico 4 - Pizza dos canais
axs[1, 1].pie(
    fat_canal.values,
    labels=fat_canal.index,
    autopct="%1.1f%%"
)
axs[1, 1].set_title("Participação por Canal")

# Formatação monetária
for ax in [axs[0, 0], axs[0, 1], axs[1, 0]]:
    ax.yaxis.set_major_formatter(
        FuncFormatter(lambda x, p: f"R$ {x:,.0f}")
    )

# Título geral
fig.suptitle(
    "Painel de Faturamento",
    fontsize=18,
    fontweight="bold"
)

plt.tight_layout()

# Ajuste para não sobrepor o título principal
plt.subplots_adjust(top=0.90)

# Salvar
plt.savefig("painel.png", dpi=150)

print("✅ painel.png criado com sucesso!")

plt.show()