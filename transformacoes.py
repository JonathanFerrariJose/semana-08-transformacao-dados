import pandas as pd

# Ler arquivo
df = pd.read_csv("clientes.csv")

# Padronizar textos
df["bairro"] = df["bairro"].str.strip().str.title()
df["plano"] = df["plano"].str.strip().str.title()

# Criar tempo de relacionamento
ano_atual = 2026
df["anos_cliente"] = ano_atual - df["ano_cadastro"]

# Classificar clientes por tempo de relacionamento
def faixa_cliente(anos):
    if anos <= 1:
        return "Novo"
    elif anos <= 3:
        return "Intermediário"
    else:
        return "Antigo"

df["faixa_cliente"] = df["anos_cliente"].apply(faixa_cliente)

# Extrair primeiro nome
df["primeiro_nome"] = df["nome"].str.split().str[0]

# Conferir planos existentes
print(df["plano"].value_counts())

# Salvar resultado
df.to_csv("clientes_transformado.csv", index=False)

print(df.head())