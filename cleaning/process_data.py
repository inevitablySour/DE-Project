import pandas as pd
import json
import sqlite3
import os
import re
from datetime import datetime
from pathlib import Path

# This file was used to produce the csv files in /cleaned data

# Create output directory
output_dir = "../cleaned_data"
Path(output_dir).mkdir(exist_ok=True)

# --- Normalization Helpers ---

def normalize_phone_number(phone):
    if pd.isnull(phone):
        return None
    phone = re.sub(r'[^\d+x]', '', phone)
    match = re.match(r'(\d{10,})(x\d+)?', phone)
    if match:
        number = match.group(1)
        ext = match.group(2) if match.group(2) else ''
        return f'+{number}{ext}'
    return phone

def standardize_date(date_str):
    if pd.isnull(date_str):
        return None
    try:
        return datetime.fromisoformat(date_str).strftime('%Y-%m-%d')
    except:
        return date_str

def clean_dataframe(df):
    for col in df.columns:
        if 'phone' in col.lower():
            df[col] = df[col].apply(normalize_phone_number)
        if 'date' in col.lower():
            df[col] = df[col].apply(standardize_date)
    return df

# --- Process CSV Files ---

print("Processing CSV files...")
patients_df = clean_dataframe(pd.read_csv("../data/patients.csv"))
observations_df = clean_dataframe(pd.read_csv("../data/observations.csv"))
procedures_df = clean_dataframe(pd.read_csv("../data/procedures.csv"))

patients_df.to_csv(os.path.join(output_dir, "patients_cleaned.csv"), index=False)
observations_df.to_csv(os.path.join(output_dir, "observations_cleaned.csv"), index=False)
procedures_df.to_csv(os.path.join(output_dir, "procedures_cleaned.csv"), index=False)

# --- Process JSON Files ---

print("Processing JSON files...")
with open("../data/diagnoses.json") as f:
    diagnoses_data = json.load(f)
diagnoses_df = clean_dataframe(pd.DataFrame(diagnoses_data))
diagnoses_df.to_csv(os.path.join(output_dir, "diagnoses_cleaned.csv"), index=False)

with open("../data/medications.json") as f:
    medications_data = json.load(f)
medications_df = clean_dataframe(pd.DataFrame(medications_data))
medications_df.to_csv(os.path.join(output_dir, "medications_cleaned.csv"), index=False)

# --- Process SQLite File ---

print("Processing SQLite file...")
conn = sqlite3.connect("../data/ehr_journeys_database.sqlite")
cursor = conn.cursor()

cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
tables = cursor.fetchall()

for table_name_tuple in tables:
    table_name = table_name_tuple[0]
    print(f"Reading table: {table_name}")
    df = pd.read_sql_query(f"SELECT * FROM {table_name}", conn)
    df_cleaned = clean_dataframe(df)
    df_cleaned.to_csv(os.path.join(output_dir, f"{table_name}_cleaned.csv"), index=False)

conn.close()

print("All files cleaned and saved to 'cleaned_data/' folder.")