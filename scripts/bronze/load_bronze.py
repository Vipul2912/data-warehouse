import pandas as pd
import mysql.connector
from pathlib import Path

conn = mysql.connector.connect(
    host="localhost",
    user="v_pulll",
    password="password",
    database="bronze"
)

cursor = conn.cursor()

files = {
    "crm_cust_info": "datasets/source_crm/cust_info.csv",
    "crm_prd_info": "datasets/source_crm/prd_info.csv",
    "crm_sales_details": "datasets/source_crm/sales_details.csv",
    "erp_cust_az12": "datasets/source_erp/CUST_AZ12.csv",
    "erp_loc_a101": "datasets/source_erp/LOC_A101.csv",
    "erp_px_cat_g1v2": "datasets/source_erp/PX_CAT_G1V2.csv"
}

base_path = Path("/home/v_pulll/datawarehouseproject/sql-data-warehouse-project")

for table, relative_path in files.items():

    full_path = base_path / relative_path

    print(f"Loading {table}...")

    cursor.execute(f"TRUNCATE TABLE {table}")

    df = pd.read_csv(full_path)

    # Convert NaN -> None
    df = df.astype(object).where(pd.notnull(df), None)

    columns = ", ".join(df.columns)

    placeholders = ", ".join(["%s"] * len(df.columns))

    insert_query = f"""
        INSERT INTO {table} ({columns})
        VALUES ({placeholders})
    """

    data = [tuple(row) for row in df.to_numpy()]

    cursor.executemany(insert_query, data)

    conn.commit()

    print(f"{table} loaded successfully.")

cursor.close()
conn.close()

print("Bronze layer ingestion completed.")
