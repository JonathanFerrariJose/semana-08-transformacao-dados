from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

# Base do projeto
BASE = Path(__file__).parent if "__file__" in globals() else Path.cwd()

# Leitura dos arquivos
pedidos = pd.read_csv(BASE / "pedidos.csv")
produtos = pd.read_csv(BASE / "produtos.csv")

# Merge sem limpeza
df = pedidos.merge(produtos, on="id_produto", how="left")

# Data e dia da semana
df["data"] = pd.to_datetime(df["data"])

nomes = ["seg", "ter", "qua", "qui", "sex", "sab", "dom"]

df["dia"] = df["data"].dt.dayofweek.map(dict(enumerate(nomes)))

# Base sem duplicados para o gráfico de contagem
unicos = df.drop_duplicates()

# Tempo abaixo de 120 min
bom = df[df["tempo_entrega_min"] < 120]

# Pasta dos gráficos
pasta = BASE / "graficos"
pasta.mkdir(exist_ok=True)

sns.set_theme(style="whitegrid")

# ==================================================
# 1 - Histograma do tempo de entrega (com extremos)
# ==================================================

plt.figure(figsize=(5, 3.6))

sns.histplot(
    df["tempo_entrega_min"].dropna(),
    bins=20
)

plt.title("Tempo de entrega (com extremos)")

plt.savefig(
    pasta / "tempo_com_extremos.png",
    dpi=120
)

plt.close()

# O que vi:
# A maioria das entregas está concentrada em valores baixos,
# mas existem observações extremas que distorcem a visualização.
#
# O que faria:
# Investigaria os valores extremos antes de calcular métricas.

# ==================================================
# 2 - Histograma sem extremos
# ==================================================

plt.figure(figsize=(5, 3.6))

sns.histplot(
    bom["tempo_entrega_min"],
    bins=15
)

plt.title("Tempo de entrega (abaixo de 120 min)")

plt.savefig(
    pasta / "tempo_sem_extremos.png",
    dpi=120
)

plt.close()

# O que vi:
# Sem os extremos, a distribuição real dos tempos
# de entrega fica mais fácil de visualizar.
#
# O que faria:
# Registraria a regra usada para remover extremos.

# ==================================================
# 3 - Boxplot de quantidade por categoria
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
    dpi=120
)

plt.close()

# O que vi:
# Existem valores muito acima do padrão em algumas categorias.
#
# O que faria:
# Verificaria se são pedidos reais ou erros de digitação.

# ==================================================
# 4 - Countplot por dia da semana
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
    dpi=120
)

plt.close()

# O que vi:
# Alguns dias concentram mais pedidos do que outros.
#
# O que faria:
# Ajustaria equipe e estoque para os dias mais movimentados.

print("Gráficos gravados em:", pasta)

for arquivo in sorted(pasta.glob("*.png")):
    print(" -", arquivo.name)