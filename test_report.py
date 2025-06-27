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
    "Q1 - Average age and age range of patients": """
        SELECT 
            AVG(EXTRACT(YEAR FROM AGE(CURRENT_DATE, date_of_birth))) AS average_age,
            MAX(EXTRACT(YEAR FROM AGE(CURRENT_DATE, date_of_birth))) - 
            MIN(EXTRACT(YEAR FROM AGE(CURRENT_DATE, date_of_birth))) AS age_range
        FROM patients;
    """,
    "Q2 - Average number of patients per physician": """
        SELECT AVG(patient_count) FROM (
            SELECT COUNT(DISTINCT patient_id) AS patient_count
            FROM encounters
            WHERE attending_physician_id IS NOT NULL
            GROUP BY attending_physician_id
        ) AS sub;
    """,
    "Q3 - Common diagnoses by patients aged 30–40": """
        SELECT d.diagnosis_description, COUNT(*) AS freq
        FROM diagnoses d
        JOIN patients p ON d.patient_id = p.patient_id
        WHERE EXTRACT(YEAR FROM AGE(CURRENT_DATE, p.date_of_birth)) BETWEEN 30 AND 40
        GROUP BY d.diagnosis_description
        ORDER BY freq DESC
        LIMIT 5;
    """,
    "Q4 - Medications per diagnosis": """
        SELECT d.diagnosis_description, COUNT(DISTINCT m.medication_order_id) AS med_count
        FROM diagnoses d
        JOIN medications m ON d.patient_id = m.patient_id
        GROUP BY d.diagnosis_description
        ORDER BY med_count DESC
        LIMIT 5;
    """,
    "Q5 - Procedures per encounter": """
        SELECT e.encounter_id, COUNT(p.procedure_id) AS procedure_count
        FROM encounters e
        JOIN procedures p ON e.encounter_id = p.encounter_id
        GROUP BY e.encounter_id
        ORDER BY procedure_count DESC
        LIMIT 5;
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