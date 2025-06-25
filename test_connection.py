import psycopg2

try:
    conn = psycopg2.connect(
        dbname="health_db",
        user="group_user",
        password="group_pass",
        host="localhost",
        port="5432"  # or "5433" if you changed it
    )
    print("✅ Connected successfully.")
    conn.close()
except Exception as e:
    print("❌ Connection failed:")
    print(e)
