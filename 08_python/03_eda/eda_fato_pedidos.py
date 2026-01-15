import os
import pandas as pd
import matplotlib.pyplot as plt

# ==========================
# CONFIGURAÇÕES
# ==========================
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
EXPORT_PATH = os.path.join(BASE_DIR, "../05_exports")

INPUT_PARQUET = os.path.join(EXPORT_PATH, "fato_pedidos_tratado.parquet")

# ==========================
# FUNÇÕES AUXILIARES
# ==========================
def detectar_colunas(df: pd.DataFrame):
    col_data = next((c for c in ["data_pedido", "data", "dt_pedido", "data_criacao"] if c in df.columns), None)
    col_valor = "valor_liquido" if "valor_liquido" in df.columns else next(
        (c for c in ["valor_total", "total", "valor", "preco_total", "receita"] if c in df.columns),
        None
    )
    return col_data, col_valor

def resumo_nulos(df: pd.DataFrame, top: int = 20):
    nulos = df.isna().sum().sort_values(ascending=False)
    nulos = nulos[nulos > 0].head(top)
    return nulos

# ==========================
# FUNÇÃO PRINCIPAL
# ==========================
def main():
    if not os.path.exists(INPUT_PARQUET):
        raise FileNotFoundError(f"Não encontrei o arquivo: {INPUT_PARQUET}")

    df = pd.read_parquet(INPUT_PARQUET)

    print("✅ EDA - Dataset carregado")
    print("Linhas e colunas:", df.shape)
    print("\n📌 Colunas:")
    print(list(df.columns))

    # Detecta colunas principais
    col_data, col_valor = detectar_colunas(df)
    print("\n🔎 Coluna de data detectada:", col_data)
    print("🔎 Coluna de valor detectada:", col_valor)

    # Info geral
    print("\n🧾 df.info():")
    print(df.info())

    # Nulos
    nulos = resumo_nulos(df)
    print("\n🧼 Nulos (top):")
    if len(nulos) == 0:
        print("Sem valores nulos 🎉")
    else:
        print(nulos)

    # Stats numéricos
    print("\n📊 Estatísticas (numéricas):")
    print(df.describe(include="number").T)

    # ==========================
    # GRÁFICOS (salvos em arquivo)
    # ==========================
    charts_dir = os.path.join(BASE_DIR, "charts")
    os.makedirs(charts_dir, exist_ok=True)

    # 1) Distribuição do valor
    if col_valor:
        plt.figure()
        df[col_valor].dropna().plot(kind="hist", bins=50)
        plt.title(f"Distribuição - {col_valor}")
        plt.xlabel(col_valor)
        plt.ylabel("Frequência")
        plt.tight_layout()
        plt.savefig(os.path.join(charts_dir, f"hist_{col_valor}.png"))
        plt.close()

    # 2) Série diária (faturamento por dia)
    if col_data and col_valor:
        serie_dia = (
            df.groupby(df[col_data].dt.date)[col_valor]
              .sum()
              .sort_index()
        )

        plt.figure()
        serie_dia.plot()
        plt.title("Faturamento por dia")
        plt.xlabel("Dia")
        plt.ylabel(col_valor)
        plt.tight_layout()
        plt.savefig(os.path.join(charts_dir, "serie_faturamento_dia.png"))
        plt.close()

    # 3) Faturamento por mês (se tiver ano_mes)
    if "ano_mes" in df.columns and col_valor:
        mensal = df.groupby("ano_mes")[col_valor].sum().sort_index()

        plt.figure()
        mensal.plot(kind="bar")
        plt.title("Faturamento por mês")
        plt.xlabel("Ano-Mês")
        plt.ylabel(col_valor)
        plt.tight_layout()
        plt.savefig(os.path.join(charts_dir, "faturamento_mensal.png"))
        plt.close()

    # 4) Outliers simples (top 10 maiores valores)
    if col_valor:
        top10 = df[[col_valor]].dropna().sort_values(by=col_valor, ascending=False).head(10)
        print("\n🚨 Top 10 maiores valores (possíveis outliers):")
        print(top10)

    print(f"\n✅ EDA concluído! Gráficos salvos em: {charts_dir}")

# ==========================
# EXECUÇÃO
# ==========================
if __name__ == "__main__":
    main()
