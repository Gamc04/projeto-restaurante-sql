import os
import pandas as pd
from google.cloud import bigquery
from google.oauth2 import service_account

PROJECT_ID = "carbide-crowbar-483718-i8"
DATASET = "restaurante"

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
CREDENTIALS_PATH = os.path.join(BASE_DIR, "../01_extract/credentials.json")
EXPORT_PATH = os.path.join(BASE_DIR, "../05_exports")

# Arquivos (ajuste se os seus nomes forem diferentes)
PATH_DIARIOS_CSV = os.path.join(EXPORT_PATH, "kpis_diarios.csv")
PATH_GERAIS_CSV = os.path.join(EXPORT_PATH, "kpis_gerais.csv")
PATH_MENSAIS_CSV = os.path.join(EXPORT_PATH, "kpis_mensais.csv")  # <-- gere em CSV também

TABLE_DIARIOS_RAW = "kpis_diarios_raw"
TABLE_GERAIS_RAW = "kpis_gerais_raw"
TABLE_MENSAIS_RAW = "kpis_mensais_raw"

VIEW_DIARIOS_GOLD = "vw_kpis_diarios_gold"
VIEW_GERAIS_GOLD = "vw_kpis_gerais_gold"
VIEW_MENSAIS_GOLD = "vw_kpis_mensais_gold"


def get_client():
    credentials = service_account.Credentials.from_service_account_file(CREDENTIALS_PATH)
    return bigquery.Client(credentials=credentials, project=PROJECT_ID)


def load_csv_as_raw(client: bigquery.Client, csv_path: str, table_raw: str, schema):
    if not os.path.exists(csv_path):
        raise FileNotFoundError(f"Arquivo não encontrado: {csv_path}")

    table_id = f"{PROJECT_ID}.{DATASET}.{table_raw}"
    client.delete_table(table_id, not_found_ok=True)
    print(f"🗑️ RAW removida (se existia): {table_id}")

    job_config = bigquery.LoadJobConfig(
        source_format=bigquery.SourceFormat.CSV,
        skip_leading_rows=1,
        write_disposition=bigquery.WriteDisposition.WRITE_TRUNCATE,
        field_delimiter=",",
        allow_quoted_newlines=True,
        schema=schema,
    )

    with open(csv_path, "rb") as f:
        job = client.load_table_from_file(f, table_id, job_config=job_config)
    job.result()

    t = client.get_table(table_id)
    print(f"✅ RAW carregada: {table_id} | linhas={t.num_rows} | cols={len(t.schema)}")
    return table_id


def create_view(client: bigquery.Client, view_name: str, sql_body: str):
    view_id = f"{PROJECT_ID}.{DATASET}.{view_name}"
    sql = f"CREATE OR REPLACE VIEW `{view_id}` AS\n{sql_body}"
    client.query(sql).result()
    print(f"✅ VIEW GOLD criada/atualizada: {view_id}")

    # count
    cnt = list(client.query(f"SELECT COUNT(*) AS c FROM `{view_id}`").result())[0]["c"]
    print(f"📌 COUNT(*) {view_id} = {cnt}")
    return view_id


def main():
    client = get_client()

    # ==========================
    # 1) DIÁRIOS (CSV -> RAW STRING -> VIEW GOLD)
    # ==========================
    raw_diarios_id = load_csv_as_raw(
        client,
        PATH_DIARIOS_CSV,
        TABLE_DIARIOS_RAW,
        schema=[
            bigquery.SchemaField("dia", "STRING"),
            bigquery.SchemaField("faturamento_diario", "STRING"),
            bigquery.SchemaField("pedidos_diarios", "STRING"),
            bigquery.SchemaField("ticket_medio_diario", "STRING"),
        ],
    )

    create_view(
        client,
        VIEW_DIARIOS_GOLD,
        f"""
SELECT
  COALESCE(
    SAFE.PARSE_DATE('%Y-%m-%d', dia),
    SAFE.PARSE_DATE('%d/%m/%Y', dia)
  ) AS dia,
  SAFE_CAST(REPLACE(faturamento_diario, ',', '.') AS FLOAT64) AS faturamento_diario,
  SAFE_CAST(pedidos_diarios AS INT64) AS pedidos_diarios,
  SAFE_CAST(REPLACE(ticket_medio_diario, ',', '.') AS FLOAT64) AS ticket_medio_diario
FROM `{raw_diarios_id}`
WHERE COALESCE(
    SAFE.PARSE_DATE('%Y-%m-%d', dia),
    SAFE.PARSE_DATE('%d/%m/%Y', dia)
) IS NOT NULL
""",
    )

    # ==========================
    # 2) GERAIS (CSV -> RAW STRING -> VIEW GOLD)
    # ==========================
    raw_gerais_id = load_csv_as_raw(
        client,
        PATH_GERAIS_CSV,
        TABLE_GERAIS_RAW,
        schema=[
            bigquery.SchemaField("faturamento_total", "STRING"),
            bigquery.SchemaField("total_pedidos", "STRING"),
            bigquery.SchemaField("ticket_medio", "STRING"),
            bigquery.SchemaField("ticket_unitario_medio", "STRING"),
            bigquery.SchemaField("quantidade_total", "STRING"),
        ],
    )

    create_view(
        client,
        VIEW_GERAIS_GOLD,
        f"""
SELECT
  SAFE_CAST(REPLACE(faturamento_total, ',', '.') AS FLOAT64) AS faturamento_total,
  SAFE_CAST(total_pedidos AS INT64) AS total_pedidos,
  SAFE_CAST(REPLACE(ticket_medio, ',', '.') AS FLOAT64) AS ticket_medio,
  SAFE_CAST(REPLACE(ticket_unitario_medio, ',', '.') AS FLOAT64) AS ticket_unitario_medio,
  SAFE_CAST(quantidade_total AS INT64) AS quantidade_total
FROM `{raw_gerais_id}`
""",
    )

    # ==========================
    # 3) MENSAIS (CSV -> RAW STRING -> VIEW GOLD)
    # ==========================
    if not os.path.exists(PATH_MENSAIS_CSV):
        raise FileNotFoundError(
            f"❌ Não achei {PATH_MENSAIS_CSV}. Gere também kpis_mensais.csv no metrics."
        )

    raw_mensais_id = load_csv_as_raw(
        client,
        PATH_MENSAIS_CSV,
        TABLE_MENSAIS_RAW,
        schema=[
            bigquery.SchemaField("ano_mes", "STRING"),
            bigquery.SchemaField("faturamento_mensal", "STRING"),
            bigquery.SchemaField("pedidos_mensais", "STRING"),
            bigquery.SchemaField("ticket_medio_mensal", "STRING"),
        ],
    )

    create_view(
        client,
        VIEW_MENSAIS_GOLD,
        f"""
SELECT
  ano_mes,
  SAFE_CAST(REPLACE(faturamento_mensal, ',', '.') AS FLOAT64) AS faturamento_mensal,
  SAFE_CAST(pedidos_mensais AS INT64) AS pedidos_mensais,
  SAFE_CAST(REPLACE(ticket_medio_mensal, ',', '.') AS FLOAT64) AS ticket_medio_mensal
FROM `{raw_mensais_id}`
""",
    )

    print("\n🚀 Tudo pronto! No Looker, use as views:")
    print(f"- {PROJECT_ID}.{DATASET}.{VIEW_GERAIS_GOLD}")
    print(f"- {PROJECT_ID}.{DATASET}.{VIEW_DIARIOS_GOLD}")
    print(f"- {PROJECT_ID}.{DATASET}.{VIEW_MENSAIS_GOLD}")


if __name__ == "__main__":
    main()
