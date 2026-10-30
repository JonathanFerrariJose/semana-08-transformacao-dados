import pandas as pd
import numpy as np


def preparar_pedidos(pedidos, produtos, clientes):

    # =========================
    # LIMPEZA
    # =========================

    pedidos["data"] = pd.to_datetime(pedidos["data"])

    pedidos["canal"] = (
        pedidos["canal"]
        .str.strip()
        .str.title()
    )

    # Padronizar canais
    pedidos["canal"] = pedidos["canal"].replace({
        "App": "App",
        "Delivery": "Delivery",
        "Balcão": "Balcão"
    })

    # Colunas de data
    pedidos["mes"] = pedidos["data"].dt.month

    pedidos["dia_semana"] = pedidos["data"].dt.day_name()

    # =========================
    # CONDICIONAIS
    # =========================

    pedidos["pedido_grande"] = np.where(
        pedidos["qtd"] >= 3,
        "Sim",
        "Não"
    )

    condicoes = [
        pedidos["qtd"] >= 3,
        pedidos["qtd"] == 2,
        pedidos["qtd"] == 1
    ]

    valores = [
        "Grande",
        "Médio",
        "Pequeno"
    ]

    pedidos["perfil"] = np.select(
        condicoes,
        valores,
        default="Revisar"
    )

    # =========================
    # JUNÇÃO COM PRODUTOS
    # =========================

    base = pedidos.merge(
        produtos,
        on="id_produto",
        how="left",
        validate="m:1"
    )

    # =========================
    # JUNÇÃO COM CLIENTES
    # =========================

    base = base.merge(
        clientes,
        on="id_cliente",
        how="left",
        indicator=True
    )

    # =========================
    # MÉTRICAS
    # =========================

    base["total"] = (
        base["qtd"] *
        base["preco"]
    )

    base["lucro"] = (
        (base["preco"] - base["custo"])
        * base["qtd"]
    )

    return base


# =========================
# EXECUÇÃO
# =========================

pedidos = pd.read_csv("pedidos.csv")
produtos = pd.read_csv("produtos.csv")
clientes = pd.read_csv("clientes.csv")

resultado = preparar_pedidos(
    pedidos,
    produtos,
    clientes
)

resultado.to_csv(
    "pedidos_prontos.csv",
    index=False
)

print("\nShape:")
print(resultado.shape)

print("\nHead:")
print(resultado.head())

print("\nPedidos sem cliente:")
print((resultado["_merge"] == "left_only").sum())
