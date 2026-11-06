import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.ticker import FuncFormatter


def criar_painel(base):
    # Conversões
    base["total"] = pd.to_numeric(base["total"], errors="coerce")
    base = base.dropna(subset=["total"])

    # Agrupamentos
    faturamento_mes = base.groupby("mes")["total"].sum()

    faturamento_categoria = (
        base.groupby("categoria")["total"]
        .sum()
        .sort_values(ascending=False)
    )

    faturamento_canal = (
        base.groupby("canal")["total"]
        .sum()
        .sort_values(ascending=False)
    )

    pedidos_categoria = (
        base.groupby("categoria")["id_pedido"]
        .count()
        .sort_values(ascending=False)
    )

    # Painel 2x2
    fig, axs = plt.subplots(2, 2, figsize=(15, 10))

    # 1. Faturamento por mês
    axs[0, 0].plot(
        faturamento_mes.index,
        faturamento_mes.values,
        marker="o",
        linewidth=2,
        color="#2E86AB"
    )
    axs[0, 0].set_title("Faturamento por Mês")
    axs[0, 0].set_xlabel("Mês")
    axs[0, 0].set_ylabel("Faturamento")

    # 2. Faturamento por categoria
    axs[0, 1].bar(
        faturamento_categoria.index,
        faturamento_categoria.values,
        color="#4CAF50"
    )
    axs[0, 1].set_title("Faturamento por Categoria")
    axs[0, 1].set_xlabel("Categoria")
    axs[0, 1].set_ylabel("Faturamento")
    axs[0, 1].tick_params(axis="x", rotation=30)

    # 3. Faturamento por canal
    axs[1, 0].bar(
        faturamento_canal.index,
        faturamento_canal.values,
        color="#FF9800"
    )
    axs[1, 0].set_title("Faturamento por Canal")
    axs[1, 0].set_xlabel("Canal")
    axs[1, 0].set_ylabel("Faturamento")

    # 4. Quantidade de pedidos por categoria
    axs[1, 1].bar(
        pedidos_categoria.index,
        pedidos_categoria.values,
        color="#9C27B0"
    )
    axs[1, 1].set_title("Pedidos por Categoria")
    axs[1, 1].set_xlabel("Categoria")
    axs[1, 1].set_ylabel("Quantidade")
    axs[1, 1].tick_params(axis="x", rotation=30)

    # Formatação monetária
    formatter = FuncFormatter(
        lambda x, p: f"R$ {x:,.0f}"
    )

    axs[0, 0].yaxis.set_major_formatter(formatter)
    axs[0, 1].yaxis.set_major_formatter(formatter)
    axs[1, 0].yaxis.set_major_formatter(formatter)

    # Grade
    for ax in axs.flat:
        ax.grid(alpha=0.3)

    # Título geral
    fig.suptitle(
        "Painel Gerencial da Cafeteria",
        fontsize=18,
        fontweight="bold"
    )

    plt.tight_layout()
    plt.subplots_adjust(top=0.90)

    plt.savefig("painel.png", dpi=150)

    print("✅ painel.png gerado com sucesso!")

    plt.show()


# ==========================
# EXECUÇÃO
# ==========================

df = pd.read_csv(
    "pedidos_prontos.csv",
    comment="<",
    on_bad_lines="skip"
)

criar_painel(df)