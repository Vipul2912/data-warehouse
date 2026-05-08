import mysql.connector

# Database connection
conn = mysql.connector.connect(
    host="localhost",
    user="v_pulll",
    password="password",
    allow_local_infile=True
)

cursor = conn.cursor()

# Read SQL file
from pathlib import Path

sql_file = Path(__file__).parent / "load_silver.sql"

with open(sql_file, "r") as file:
    sql_script = file.read()

# Split queries by semicolon
queries = sql_script.split(';')

# Execute each query
for query in queries:
    query = query.strip()

    if query:
        try:
            cursor.execute(query)
            conn.commit()
            print(f"Executed successfully:\n{query[:80]}...\n")

        except Exception as e:
            print(f"Error executing query:\n{query[:80]}...\n")
            print(e)

cursor.close()
conn.close()

print("Silver layer loaded successfully.")
