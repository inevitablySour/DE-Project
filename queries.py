import pandas as pd
from sqlalchemy import create_engine

engine = create_engine("postgresql+psycopg2://group_user:group_pass@localhost:5433/health_db")

queries = {
    "Q1_AgeStats": """
        SELECT 
            ROUND(AVG(EXTRACT(YEAR FROM AGE(current_date, date_of_birth)))) AS avg_age,
            MIN(EXTRACT(YEAR FROM AGE(current_date, date_of_birth))) AS min_age,
            MAX(EXTRACT(YEAR FROM AGE(current_date, date_of_birth))) AS max_age
        FROM patients;
    """,
    "Q2_PatientsPerPhysician": """
        SELECT 
            attending_physician_id, 
            COUNT(DISTINCT patient_id) AS unique_patients
        FROM encounters
        GROUP BY attending_physician_id;
    """,
    "Q3_CommonDiagnosesByAge": """
        SELECT 
            diagnosis_description,
            ROUND(EXTRACT(YEAR FROM AGE(current_date, p.date_of_birth)) / 10) * 10 AS age_group,
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
    "Q5_ProceduresPerEncounter": """
        SELECT 
            p.patient_id,
            COUNT(DISTINCT pr.procedure_id) / COUNT(DISTINCT e.encounter_id)::float AS avg_procedures_per_encounter
        FROM procedures pr
        JOIN encounters e ON pr.encounter_id = e.encounter_id
        JOIN patients p ON e.patient_id = p.patient_id
        GROUP BY p.patient_id
        ORDER BY avg_procedures_per_encounter DESC;
    """
}

# Run and export each query
for name, query in queries.items():
    print(f"Running: {name}")
    df = pd.read_sql(query, engine)
    df.to_csv(f"output/{name}.csv", index=False)
    print(f"Saved results to output/{name}.csv")