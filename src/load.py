
import pandas as pd
import pyodbc
from pathlib import Path


# STEP 1: Connect to SQL Server
def connect_database():

    connection = pyodbc.connect(
        "DRIVER={ODBC Driver 18 for SQL Server};"
        "SERVER=.\\SQLEXPRESS;"
        "DATABASE=GermanITJobMarket;"
        "Trusted_Connection=yes;"
        "Encrypt=yes;"
        "TrustServerCertificate=yes;"
    )

    print("SQL Server connection successful!")
    return connection


# STEP 2: Prepare data for SQL Server
def prepare_data(df):

    prepared_jobs = df.copy()

    # Convert missing values to Python None
    prepared_jobs = (
        prepared_jobs.astype(object)
        .where(pd.notna(prepared_jobs), None)
    )

    # Convert posted_date to Python date
    prepared_jobs["posted_date"] = (
        prepared_jobs["posted_date"].apply(
            lambda x: x.date() if x is not None else None
        )
    )

    # Convert fetched_at to ISO timestamp
    prepared_jobs["fetched_at"] = (
        prepared_jobs["fetched_at"].apply(
            lambda x: x.isoformat() if x is not None else None
        )
    )

    return prepared_jobs


# STEP 3: Load data into SQL Server
def load_data(df, connection):

    columns = [
        "id", "source", "source_url", "license", "provenance",
        "fetched_at", "posted_date", "lang", "title", "employer",
        "region", "nuts_code", "esco_occupation", "esco_skills",
        "is_green", "kldb_2010", "seniority", "salary_range"
    ]

    # Ensure columns match SQL INSERT order
    df = df[columns]

    cursor = connection.cursor()

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

    for row in df.itertuples(index=False, name=None):
        rows.append(row + (row[0],))

    try:
        cursor.executemany(insert_query, rows)
        connection.commit()
        print("Database load completed successfully!")

    except Exception as e:
        connection.rollback()
        print("Database load failed:", e)
        raise

    finally:
        cursor.close()


# STEP 4: Test the complete loading process
if __name__ == "__main__":

    from extract import extract_data
    from transform import (
        filter_it_jobs,
        clean_job_data,
        filter_german_regions
    )
    from validate import (
        validate_job_ids,
        validate_required_columns,
        validate_blank_values
    )

    project_folder = Path(__file__).resolve().parent.parent
    csv_path = project_folder / "german_jobs.csv"

    # Extract
    df = extract_data(csv_path)

    # Transform
    it_jobs = filter_it_jobs(df)
    cleaned_jobs = clean_job_data(it_jobs)
    german_jobs = filter_german_regions(cleaned_jobs)

    # Validate
    validate_job_ids(german_jobs)
    validate_required_columns(german_jobs)
    validate_blank_values(german_jobs)

    # Prepare
    prepared_jobs = prepare_data(german_jobs)

    # Load
    connection = connect_database()

    try:
        load_data(prepared_jobs, connection)
    finally:
        connection.close()

    print("Load process finished!")
