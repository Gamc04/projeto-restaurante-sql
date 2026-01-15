import os
import pandas as pd
from google.cloud import bigquery
from google.oauth2 import service_account

PROJECT_ID = "carbide-crowbar-483718-i8"
DATASET = "restaurante"
VIEW = "fato_pedidos"

# Caminho do JSON (mesma pasta do script)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
CREDENTIALS_PATH = os.path.join(BASE_DIR, "credentials.json")


def main():
    # Cria credencial a partir do JSON
    credentials = service_account.Credentials.from_service_account_file(
        CREDENTIALS_PATH
    )

    # Cliente BigQuery autenticado
    client = bigquery.Client(
        credentials=credentials,
        project=PROJECT_ID
    )

    query = f"""
        SELECT *
        FROM `{PROJECT_ID}.{DATASET}.{VIEW}`
    """

    df = client.query(query).to_dataframe()


    if "data_pedido" in df.columns:
        df["data_pedido"] = pd.to_datetime(df["data_pedido"], errors="coerce")

    # Cria pasta de export se não existir
    export_path = os.path.join(BASE_DIR, "../05_exports")
    os.makedirs(export_path, exist_ok=True)

    # Exporta dados
    df.to_parquet(
        os.path.join(export_path, "fato_pedidos.parquet"),
        index=False
    )
    df.to_csv(
        os.path.join(export_path, "fato_pedidos.csv"),
        index=False,
        encoding="utf-8"
    )

    print("✅ Extração concluída com sucesso!")
    print("Linhas e colunas:", df.shape)
    print(df.head())


if __name__ == "__main__":
    main()
