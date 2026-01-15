import os
import pandas as pd


INPUT_PARQUET = "fato_pedidos.parquet"
INPUT_CSV = "fato_pedidos.csv"

OUTPUT_PARQUET = "fato_pedidos_tratado.parquet"
OUTPUT_CSV = "fato_pedidos_tratado.csv"

# Caminho base (mesma pasta do script)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Pastas padrão (seguindo sua linha)
EXPORT_PATH = os.path.join(BASE_DIR, "../05_exports")
os.makedirs(EXPORT_PATH, exist_ok=True)


def padronizar_colunas(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    df.columns = (
        df.columns
          .astype(str)
          .str.strip()
          .str.lower()
          .str.replace(" ", "_")
    )
    return df

def converter_tipos_e_limpar(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()


    possiveis_datas = ["data_pedido", "data", "dt_pedido", "data_criacao"]
    for col in possiveis_datas:
        if col in df.columns:
            df[col] = pd.to_datetime(df[col], errors="coerce")


    possiveis_valores = ["valor_total", "total", "valor", "preco_total", "receita"]
    for col in possiveis_valores:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors="coerce")

    if "desconto" in df.columns:
        df["desconto"] = pd.to_numeric(df["desconto"], errors="coerce").fillna(0)

    if "quantidade" in df.columns:
        df["quantidade"] = pd.to_numeric(df["quantidade"], errors="coerce")



    col_data = next((c for c in ["data_pedido", "data", "dt_pedido", "data_criacao"] if c in df.columns), None)
    col_valor = next((c for c in ["valor_total", "total", "valor", "preco_total", "receita"] if c in df.columns), None)

    subset_drop = []
    if col_data: subset_drop.append(col_data)
    if col_valor: subset_drop.append(col_valor)

    if subset_drop:
        df = df.dropna(subset=subset_drop)

    return df

def criar_colunas_derivadas(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()


    col_data = next((c for c in ["data_pedido", "data", "dt_pedido", "data_criacao"] if c in df.columns), None)
    col_valor = next((c for c in ["valor_total", "total", "valor", "preco_total", "receita"] if c in df.columns), None)

    # Valor líquido
    if col_valor:
        if "desconto" in df.columns:
            df["valor_liquido"] = df[col_valor] - df["desconto"]
        else:
            df["valor_liquido"] = df[col_valor]

    # Dimensões de tempo
    if col_data:
        df["ano"] = df[col_data].dt.year
        df["mes"] = df[col_data].dt.month
        df["dia"] = df[col_data].dt.day
        df["dia_semana"] = df[col_data].dt.day_name()


        df["ano_mes"] = df[col_data].dt.to_period("M").astype(str)

    if "valor_liquido" in df.columns and "quantidade" in df.columns:
        # evita divisão por zero
        df["ticket_unitario"] = df["valor_liquido"] / df["quantidade"].replace(0, pd.NA)

    return df

def validar(df: pd.DataFrame) -> None:

    if "valor_liquido" in df.columns:

        min_val = df["valor_liquido"].min()
        assert pd.isna(min_val) or min_val >= 0, f"valor_liquido negativo encontrado: {min_val}"


def main():
    parquet_path = os.path.join(EXPORT_PATH, INPUT_PARQUET)
    csv_path = os.path.join(EXPORT_PATH, INPUT_CSV)


    if os.path.exists(parquet_path):
        df = pd.read_parquet(parquet_path)
        fonte = "parquet"
    elif os.path.exists(csv_path):
        df = pd.read_csv(csv_path, encoding="utf-8")
        fonte = "csv"
    else:
        raise FileNotFoundError(
            f"Não encontrei {INPUT_PARQUET} nem {INPUT_CSV} em: {EXPORT_PATH}"
        )

    print(f"📥 Fonte carregada: {fonte}")
    print("Linhas e colunas (raw):", df.shape)

    # Pipeline de transformação
    df = padronizar_colunas(df)
    df = converter_tipos_e_limpar(df)
    df = criar_colunas_derivadas(df)
    validar(df)

    # Exporta tratado
    df.to_parquet(os.path.join(EXPORT_PATH, OUTPUT_PARQUET), index=False)
    df.to_csv(os.path.join(EXPORT_PATH, OUTPUT_CSV), index=False, encoding="utf-8")

    print("✅ Transformação concluída com sucesso!")
    print("Linhas e colunas (tratado):", df.shape)
    print(df.head())


if __name__ == "__main__":
    main()
