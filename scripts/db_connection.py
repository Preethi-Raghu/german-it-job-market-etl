import pyodbc

connection = pyodbc.connect(
    "DRIVER={ODBC Driver 18 for SQL Server};"
    "SERVER=.\\SQLEXPRESS;"
    "DATABASE=GermanITJobMarket;"
    "Trusted_Connection=yes;"
    "Encrypt=yes;"
    "TrustServerCertificate=yes;"
)

print("Connected to SQL Server successfully!")
cursor = connection.cursor()

cursor.execute("SELECT COUNT(*) FROM dbo.JobPostings")

result = cursor.fetchone()

print("Total records in SQL Server:", result[0])




# german_jobs["kldb_2010"] = (
#     german_jobs["kldb_2010"]
#     .astype("Int64")
#     .astype("string")
# )

# print(german_jobs["kldb_2010"].head(10))

# print("Data type:", german_jobs["kldb_2010"].dtype)

# print("Missing values:", german_jobs["kldb_2010"].isnull().sum())

import pandas as pd
from pathlib import Path

folder = Path(__file__).resolve().parent
load_jobs = pd.read_pickle(folder / "prepared_jobs.pkl")



insert_query = """
INSERT INTO dbo.JobPostings (
    id, source, source_url, license, provenance,
    fetched_at, posted_date, lang, title, employer,
    region, nuts_code, esco_occupation, esco_skills,
    is_green, kldb_2010, seniority, salary_range
)
SELECT
    ?, ?, ?, ?, ?,
    CONVERT(DATETIMEOFFSET(7), ?, 127), ?, ?, ?, ?,
    ?, ?, ?, ?,
    ?, ?, ?, ?
WHERE NOT EXISTS (
    SELECT 1
    FROM dbo.JobPostings
    WHERE id = ?
)
"""
rows = []

for row in load_jobs.itertuples(index=False, name=None):
    rows.append(row + (row[0],))

print("Rows prepared:", len(rows))
print("Parameters in first row:", len(rows[0]))
print("SQL placeholders:", insert_query.count("?"))

try:
    cursor.executemany(insert_query, rows)
    connection.commit()
    print("Batch insertion completed!")

except Exception as e:
    connection.rollback()
    print("Batch insertion failed:", e)
    raise
   
    

cursor.close()
connection.close()