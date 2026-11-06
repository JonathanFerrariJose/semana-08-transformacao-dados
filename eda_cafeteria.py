from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

# ==================================================
# CONFIGURAÇÃO
# ==================================================

BASE = Path(__file__).parent if "__file__" in globals() else Path.cwd()

pedidos = pd.read_csv(BASE / "pedidos.csv")
produtos = pd.read_csv(BASE / "produtos.csv")

df = pedidos.merge(produtos, on="id_produto", how="left")

df["data"] = pd.to_datetime(df["data"])

nomes = ["seg", "ter", "qua", "qui", "sex", "sab", "dom"]

df["dia"] = df["data"].dt.dayofweek.map(dict(enumerate(nomes)))

unicos = df.drop_duplicates()

bom = df[df["tempo_entrega_min"] < 120]

pasta = BASE / "graficos"
pasta.mkdir(exist_ok=True)

sns.set_theme(style="whitegrid")

# ==================================================
# HISTOGRAMA COM EXTREMOS
# ==================================================

plt.figure(figsize=(5, 3.6))

sns.histplot(
    df["tempo_entrega_min"].dropna(),
    bins=20
)

plt.title("Tempo de entrega (com extremos)")

plt.savefig(
    pasta / "tempo_com_extremos.png",
    dpi=120,
    bbox_inches="tight"
)

plt.close()

# ==================================================
# HISTOGRAMA SEM EXTREMOS
# ==================================================

plt.figure(figsize=(5, 3.6))

sns.histplot(
    bom["tempo_entrega_min"].dropna(),
    bins=15
)

plt.title("Tempo de entrega (abaixo de 120 min)")

plt.savefig(
    pasta / "tempo_sem_extremos.png",
    dpi=120,
    bbox_inches="tight"
)

plt.close()

# ==================================================
# BOXPLOT
# ==================================================

plt.figure(figsize=(5, 3.6))

sns.boxplot(
    data=df,
    x="categoria",
    y="qtd"
)

plt.title("Quantidade por categoria")

plt.savefig(
    pasta / "boxplot_qtd.png",
    dpi=120,
    bbox_inches="tight"
)

plt.close()

# ==================================================
# COUNTPLOT
# ==================================================

plt.figure(figsize=(5, 3.6))

sns.countplot(
    data=unicos,
    x="dia",
    order=nomes
)

plt.title("Pedidos por dia da semana")

plt.savefig(
    pasta / "pedidos_por_dia.png",
    dpi=120,
    bbox_inches="tight"
)

plt.close()

# ==================================================
# RELATÓRIO
# ==================================================

duplicados = df.duplicated().sum()
faltantes_tempo = df["tempo_entrega_min"].isna().sum()
faltantes_avaliacao = df["avaliacao"].isna().sum()

relatorio = f"""
# Relatório EDA - Cafeteria

## Tabela de Problemas

| Problema | Quantidade | Decisão |
|-----------|-----------:|----------|
| Registros duplicados | {duplicados} | Remover antes das análises finais |
| Valores ausentes em tempo_entrega_min | {faltantes_tempo} | Avaliar preenchimento ou remoção |
| Valores ausentes em avaliacao | {faltantes_avaliacao} | Não utilizar para métricas sem tratamento |

## Achados do Negócio

1. A maior parte das entregas está concentrada abaixo de 120 minutos.

2. Existem pedidos com quantidades acima do padrão observado.

3. Há diferença de volume de pedidos entre os dias da semana, sugerindo ajuste operacional.
"""

with open(BASE / "RELATORIO_EDA.md", "w", encoding="utf-8") as arquivo:
    arquivo.write(relatorio)

print("\n✅ Processo concluído com sucesso!\n")

print("Arquivos gerados:")

for arquivo in sorted(pasta.glob("*.png")):
    print(" -", arquivo.name)

print(" - RELATORIO_EDA.md")