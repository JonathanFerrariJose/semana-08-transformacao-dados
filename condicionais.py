import pandas as pd
import numpy as np

# Ler arquivo
df = pd.read_csv("clientes.csv")

# 1. np.where() -------------------------
# Cliente antigo: cadastro até 2022

df["cliente_antigo"] = np.where(
    df["ano_cadastro"] <= 2022,
    "Sim",
    "Não"
)

# 2. np.select() ------------------------
# Perfil do cliente

condicoes = [
    df["plano"] == "Premium",
    df["plano"] == "Fidelidade",
    df["plano"] == "Gratuito"
]

valores = [
    "VIP",
    "Fiel",
    "Básico"
]

df["perfil"] = np.select(condicoes, valores, default="Não informado")

# 3. .loc[] -----------------------------
# Faixa de relacionamento

df["faixa_relacionamento"] = "Recente"

df.loc[df["ano_cadastro"] <= 2023, "faixa_relacionamento"] = "Experiente"

df.loc[df["ano_cadastro"] <= 2022, "faixa_relacionamento"] = "Veterano"

# 4. pd.cut() ---------------------------
# Criar faixas de ano de cadastro

df["grupo_cadastro"] = pd.cut(
    df["ano_cadastro"],
    bins=[2020, 2022, 2024, 2026],
    labels=["2021-2022", "2023-2024", "2025-2026"]
)

# Contagens
print("\nCliente Antigo")
print(df["cliente_antigo"].value_counts())

print("\nPerfil")
print(df["perfil"].value_counts())

print("\nFaixa Relacionamento")
print(df["faixa_relacionamento"].value_counts())

print("\nGrupo Cadastro")
print(df["grupo_cadastro"].value_counts())

# Salvar
df.to_csv("clientes_classificados.csv", index=False)

print("\nArquivo gerado com sucesso!")