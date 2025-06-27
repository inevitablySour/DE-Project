import pandas as pd
from sqlalchemy import create_engine

engine = create_engine("postgresql+psycopg2://group_user:group_pass@localhost:5433/health_db")

queries = {
    "Q1_AgeStats": """
        SELECT 
            ROUND(AVG(age), 1) AS average_age,
            MIN(age) AS youngest_age,
            MAX(age) AS oldest_age,
            MAX(age) - MIN(age) AS age_range
        FROM patients;
    """,
    "Q2_PatientsPerPhysician": """
        SELECT 
            ROUND(AVG(patient_count), 1) AS avg_patients_per_physician
        FROM (
            SELECT 
                attending_physician_id, 
                COUNT(DISTINCT patient_id) AS patient_count
            FROM encounters
            GROUP BY attending_physician_id
        ) AS sub;
    """,
    "Q3_CommonDiagnosesByAge": """
        SELECT 
            diagnosis_description,
            ROUND(p.age / 10.0) * 10 AS age_group,
            COUNT(*) AS count
        FROM diagnoses d
        JOIN patients p ON d.patient_id = p.patient_id
        GROUP BY age_group, diagnosis_description
        ORDER BY age_group, count DESC;
    """,
    "Q4_MedicationPerDiagnosis": """
        SELECT 
            d.diagnosis_description, 
            m.drug_name, 
            COUNT(*) AS times_prescribed
        FROM diagnoses d
        JOIN encounters e ON d.encounter_id = e.encounter_id
        JOIN medications m ON e.encounter_id = m.encounter_id
        GROUP BY d.diagnosis_description, m.drug_name
        ORDER BY times_prescribed DESC;
    """,
    "Q5_TopProcedures": """
        SELECT 
        procedure_description,
        COUNT(*) AS times_performed
        FROM procedures
        GROUP BY procedure_description
        ORDER BY times_performed DESC;
    """
}

# Run and export each query
for name, query in queries.items():
    print(f"Running: {name}")
    df = pd.read_sql(query, engine)
    df.to_csv(f"output/{name}.csv", index=False)
    print(f"Saved results to output/{name}.csv")