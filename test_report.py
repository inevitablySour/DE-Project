import psycopg2
import time


DB_CONFIG = {
    'dbname': 'health_db',
    'user': 'group_user',
    'password': 'group_pass',
    'host': 'localhost',
    'port': 5433,
}

# Expected tables
EXPECTED_TABLES = [
    'patients',
    'encounters',
    'observations',
    'diagnoses',
    'procedures',
    'medications'
]

# Required queries
QUERIES = {
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
    "Q5_Top Procedures": """
        SELECT 
        procedure_description,
        COUNT(*) AS times_performed
        FROM procedures
        GROUP BY procedure_description
        ORDER BY times_performed DESC;
    """
}

def run_system_test(cursor):
    print("\n=== System Test: Table Existence and Row Counts ===")
    for table in EXPECTED_TABLES:
        try:
            cursor.execute(f"SELECT COUNT(*) FROM {table};")
            count = cursor.fetchone()[0]
            print(f"Table '{table}' exists with {count} rows.")
        except Exception as e:
            print(f"Table '{table}' check failed: {e}")

def run_query_tests(cursor):
    print("\n=== Query Performance Tests ===")
    for name, query in QUERIES.items():
        try:
            print(f"\nRunning {name}...")
            start = time.time()
            cursor.execute(query)
            results = cursor.fetchall()
            duration = time.time() - start
            print(f"Success: {name}")
            print(f"Execution time: {duration:.4f} seconds")
            print(f"Sample result: {results[:1]}")
        except Exception as e:
            print(f"Failed to run {name}: {e}")

def main():
    print("Connecting to the database...")
    try:
        conn = psycopg2.connect(**DB_CONFIG)
        cursor = conn.cursor()
        print("Database connection successful.")

        run_system_test(cursor)
        run_query_tests(cursor)

    except Exception as e:
        print(f"Could not connect to database: {e}")
    finally:
        if 'conn' in locals():
            conn.close()
            print("\nDatabase connection closed.")

if __name__ == "__main__":
    main()