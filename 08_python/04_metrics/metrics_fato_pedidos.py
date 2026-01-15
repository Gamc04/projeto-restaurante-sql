import os
import pandas as pd

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
EXPORT_PATH = os.path.join(BASE_DIR, "../05_exports")

PATH_FATO = os.path.join(EXPORT_PATH, "fato_pedidos.parquet")

OUT_KPIS_GERAIS_CSV = os.path.join(EXPORT_PATH, "kpis_gerais.csv")
OUT_KPIS_DIARIOS_CSV = os.path.join(EXPORT_PATH, "kpis_diarios.csv")
OUT_KPIS_MENSAIS_CSV = os.path.join(EXPORT_PATH, "kpis_mensais.csv")


def pick_valor_col(df: pd.DataFrame) -> str:
    """Escolhe a coluna de valor na ordem: valor_liquido, receita, ou calcula."""
    if "valor_liquido" in df.columns:
        return "valor_liquido"
    if "receita" in df.columns:
        return "receita"
    # fallback: quantidade * preco_unitario
    if "quantidade" in df.columns and "preco_unitario" in df.columns:
        # tenta converter preco_unitario para número (aceita "12,50" e "12.50")
        pu = (
            df["preco_unitario"]
            .astype(str)
            .str.replace(".", "", regex=False)   # remove separador de milhar
            .str.replace(",", ".", regex=False)  # vírgula -> ponto
        )
        df["preco_unitario_num"] = pd.to_numeric(pu, errors="coerce")
        df["valor_calc"] = df["preco_unitario_num"] * pd.to_numeric(df["quantidade"], errors="coerce")
        return "valor_calc"

    raise ValueError(
        "❌ Não encontrei coluna de valor. "
        "Preciso de 'valor_liquido' ou 'receita' ou ('quantidade' e 'preco_unitario')."
    )


def main():
    if not os.path.exists(PATH_FATO):
        raise FileNotFoundError(f"❌ Arquivo não encontrado: {PATH_FATO}")

    df = pd.read_parquet(PATH_FATO)

    if "data_pedido" not in df.columns:
        raise ValueError("❌ Coluna 'data_pedido' não existe no dataset.")

    # data
    df["data_pedido"] = pd.to_datetime(df["data_pedido"], errors="coerce")
    if df["data_pedido"].isna().any():
        raise ValueError("❌ Existem datas inválidas em 'data_pedido'.")

    # define coluna de valor
    valor_col = pick_valor_col(df)
    print(f"✅ Coluna de valor escolhida: {valor_col}")

    # dia
    df["dia"] = df["data_pedido"].dt.date

    # id_pedido (se não existir, usa a linha como "pedido")
    has_id_pedido = "id_pedido" in df.columns

    # ==========================
    # 1) KPIs Gerais
    # ==========================
    faturamento_total = float(pd.to_numeric(df[valor_col], errors="coerce").fillna(0).sum())
    total_pedidos = int(df["id_pedido"].nunique()) if has_id_pedido else int(len(df))
    ticket_medio = float(faturamento_total / total_pedidos) if total_pedidos > 0 else 0.0

    ticket_unitario_medio = None
    if "ticket_unitario" in df.columns:
        ticket_unitario_medio = float(pd.to_numeric(df["ticket_unitario"], errors="coerce").mean())

    quantidade_total = None
    if "quantidade" in df.columns:
        quantidade_total = int(pd.to_numeric(df["quantidade"], errors="coerce").fillna(0).sum())

    df_gerais = pd.DataFrame([{
        "faturamento_total": faturamento_total,
        "total_pedidos": total_pedidos,
        "ticket_medio": ticket_medio,
        "ticket_unitario_medio": ticket_unitario_medio,
        "quantidade_total": quantidade_total,
    }])

    # ==========================
    # 2) KPIs Diários
    # ==========================
    if has_id_pedido:
        df_diarios = (
            df.groupby("dia", as_index=False)
              .agg(
                  faturamento_diario=(valor_col, "sum"),
                  pedidos_diarios=("id_pedido", "nunique"),
              )
        )
    else:
        df_diarios = (
            df.groupby("dia", as_index=False)
              .agg(
                  faturamento_diario=(valor_col, "sum"),
                  pedidos_diarios=(valor_col, "size"),
              )
        )

    df_diarios["ticket_medio_diario"] = df_diarios["faturamento_diario"] / df_diarios["pedidos_diarios"]
    df_diarios = df_diarios.sort_values("dia")

    # formato ideal para BigQuery CSV
    df_diarios["dia"] = pd.to_datetime(df_diarios["dia"]).dt.strftime("%Y-%m-%d")

    # ==========================
    # 3) KPIs Mensais
    # ==========================
    df["ano_mes"] = df["data_pedido"].dt.strftime("%Y-%m")

    if has_id_pedido:
        df_mensais = (
            df.groupby("ano_mes", as_index=False)
              .agg(
                  faturamento_mensal=(valor_col, "sum"),
                  pedidos_mensais=("id_pedido", "nunique"),
              )
        )
    else:
        df_mensais = (
            df.groupby("ano_mes", as_index=False)
              .agg(
                  faturamento_mensal=(valor_col, "sum"),
                  pedidos_mensais=(valor_col, "size"),
              )
        )

    df_mensais["ticket_medio_mensal"] = df_mensais["faturamento_mensal"] / df_mensais["pedidos_mensais"]
    df_mensais = df_mensais.sort_values("ano_mes")

    # ==========================
    # EXPORTS (CSV)
    # ==========================
    os.makedirs(EXPORT_PATH, exist_ok=True)

    df_gerais.to_csv(OUT_KPIS_GERAIS_CSV, index=False, encoding="utf-8")
    df_diarios.to_csv(OUT_KPIS_DIARIOS_CSV, index=False, encoding="utf-8")
    df_mensais.to_csv(OUT_KPIS_MENSAIS_CSV, index=False, encoding="utf-8")

    print("\n✅ KPIs exportados em CSV com sucesso!")
    print("📌 kpis_gerais:", df_gerais.shape, "->", OUT_KPIS_GERAIS_CSV)
    print("📌 kpis_diarios:", df_diarios.shape, "->", OUT_KPIS_DIARIOS_CSV)
    print(df_diarios.head())
    print("📌 kpis_mensais:", df_mensais.shape, "->", OUT_KPIS_MENSAIS_CSV)


if __name__ == "__main__":
    main()
