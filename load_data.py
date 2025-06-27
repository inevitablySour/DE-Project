import pandas as pd
from sqlalchemy import create_engine
import os

# Set up PostgreSQL connection
engine = create_engine(
    "postgresql+psycopg2://group_user:group_pass@localhost:5433/health_db"
)

# Define base folder for the data
base_dir = os.path.dirname(__file__)
data_dir = os.path.join(base_dir, "v2cleaned_data")

# Map table names to their corresponding .parquet files
parquet_table_map = {
    "patients": "patients.parquet",
    "encounters": "encounters.parquet",
    "observations": "observations.parquet",
    "diagnoses": "diagnoses.parquet",
    "procedures": "procedures.parquet",
    "medications": "medications.parquet"
}

# Load and insert each table
for table, filename in parquet_table_map.items():
    file_path = os.path.join(data_dir, filename)
    print(f"Loading {file_path} into table '{table}'...")
    df = pd.read_parquet(file_path, engine="pyarrow")
    df.to_sql(table, engine, if_exists='append', index=False, method='multi')
    print(f"Finished importing '{table}'.")

print("All tables imported successfully.")