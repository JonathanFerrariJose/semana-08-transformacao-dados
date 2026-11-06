import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.ticker import FuncFormatter

# Ler arquivo ignorando a linha de conflito do Git
df = pd.read_csv(
    "pedidos_prontos.csv",
    comment="<",
    on_bad_lines="skip"
)

# Converter total para número
df["total"] = pd.to_numeric(df["total"], errors="coerce")

# Remover valores nulos
df = df.dropna(subset=["categoria", "total"])

# Agrupar faturamento por categoria
faturamento = (
    df.groupby("categoria")["total"]
    .sum()
    .sort_values(ascending=False)
)

# Categoria com maior faturamento
maior_categoria = faturamento.idxmax()

# Cores
cores = [
    "orange" if categoria == maior_categoria
    else "steelblue"
    for categoria in faturamento.index
]

# Criar gráfico
plt.figure(figsize=(10, 6))

barras = plt.bar(
    faturamento.index,
    faturamento.values,
    color=cores
)

# Título
plt.title(
    "Faturamento por Categoria",
    fontsize=16,
    fontweight="bold"
)

# Rótulos
plt.xlabel("Categoria")
plt.ylabel("Faturamento (R$)")

# Formatar eixo Y em reais
plt.gca().yaxis.set_major_formatter(
    FuncFormatter(
        lambda x, p: f"R$ {x:,.2f}"
    )
)

# Destacar maior barra
for barra, categoria in zip(barras, faturamento.index):
    if categoria == maior_categoria:
        plt.annotate(
            f"Maior: {categoria}",
            (
                barra.get_x() + barra.get_width() / 2,
                barra.get_height()
            ),
            ha="center",
            xytext=(0, 10),
            textcoords="offset points",
            color="red",
            fontweight="bold"
        )

# Melhorar visualização
plt.xticks(rotation=20)
plt.grid(axis="y", linestyle="--", alpha=0.4)

plt.tight_layout()

# Salvar arquivo
plt.savefig("categoria.png", dpi=150)

print("✅ categoria.png criada com sucesso!")

plt.show()