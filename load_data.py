import pandas as pd
from sqlalchemy import create_engine

# Set up connection string for PostgreSQL
engine = create_engine(
    "postgresql+psycopg2://group_user:group_pass@localhost:5432/health_db"
)

# List of CSV files and their corresponding table names
csv_table_map = {
    "patients": "cleaned_data/patients_cleaned.csv",
    "encounters": "cleaned_data/encounters_cleaned.csv",
    "observations": "cleaned_data/observations_cleaned.csv",
    "diagnoses": "cleaned_data/diagnoses_cleaned.csv",
    "procedures": "cleaned_data/procedures_cleaned.csv",
    "medications": "cleaned_data/medications_cleaned.csv"
}

# Loop through and import each CSV
for table, file_path in csv_table_map.items():
    print(f"Loading {file_path} into {table}...")
    df = pd.read_csv(file_path)
    df.to_sql(table, engine, if_exists='append', index=False, method='multi')
    print(f"Done with {table}")