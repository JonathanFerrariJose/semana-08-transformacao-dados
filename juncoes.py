import pandas as pd

# Ler arquivos
pedidos = pd.read_csv("pedidos.csv")
produtos = pd.read_csv("produtos.csv")
clientes = pd.read_csv("clientes.csv")

print("Pedidos:", len(pedidos))
print("Produtos:", len(produtos))
print("Clientes:", len(clientes))

# Merge pedidos + produtos
base = pedidos.merge(
    produtos,
    on="id_produto",
    how="left",
    validate="m:1"
)

print("\nLinhas após merge com produtos:")
print(len(base))

# Merge com clientes
base = base.merge(
    clientes,
    on="id_cliente",
    how="left",
    indicator=True
)

print("\nLinhas após merge com clientes:")
print(len(base))

# Pedidos sem cliente
sem_cliente = (base["_merge"] == "left_only").sum()

print("\nPedidos sem cliente:")
print(sem_cliente)

# Coluna total
base["total"] = base["qtd"] * base["preco"]

# Coluna lucro
base["lucro"] = (
    (base["preco"] - base["custo"])
    * base["qtd"]
)

# Lucro por categoria
lucro_categoria = (
    base.groupby("categoria")["lucro"]
    .sum()
    .sort_values(ascending=False)
)

print("\nLucro por categoria:")
print(lucro_categoria)

# Salvar resultado
base.to_csv("base_completa.csv", index=False)

print("\nArquivo base_completa.csv gerado com sucesso!")