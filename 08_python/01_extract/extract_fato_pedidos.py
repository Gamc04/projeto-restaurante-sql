import pandas as pd
from google.cloud import bigquery
from pathlib import Path

PROJECT_ID = "carbide-crowbar-483718-i8"
DATASET = "restaurante"
VIEW = "fato_pedidos"

def main():
    print("Iniciando extração do BigQuery...")

    client = bigquery.Client(project=PROJECT_ID)

    query = f"""
    SELECT *
    FROM `{PROJECT_ID}.{DATASET}.{VIEW}`
    """

    print("Executando query...")
    df = client.query(query).to_dataframe()
    print("Query executada. Convertendo para DataFrame...")

    export_dir = Path(__file__).resolve().parents[1] / "05_exports"
    export_dir.mkdir(parents=True, exist_ok=True)

    df.to_parquet(export_dir / "fato_pedidos.parquet", index=False)
    df.to_csv(export_dir / "fato_pedidos.csv", index=False, encoding="utf-8")

    print("✅ Extração concluída!")
    print("Shape:", df.shape)
    print(df.head())

if __name__ == "__main__":
    main()
