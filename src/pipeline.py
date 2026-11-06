
from pathlib import Path

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

from load import (
    connect_database,
    prepare_data,
    load_data
)


def run_pipeline():

    project_folder = Path(__file__).resolve().parent.parent
    csv_path = project_folder / "german_jobs.csv"

    # STEP 1: Extract
    print("Starting extraction...")
    df = extract_data(csv_path)
    print("Extracted records:", len(df))

    # STEP 2: Transform
    print("Starting transformation...")
    it_jobs = filter_it_jobs(df)
    cleaned_jobs = clean_job_data(it_jobs)
    german_jobs = filter_german_regions(cleaned_jobs)
    print("Transformed records:", len(german_jobs))

    # STEP 3: Validate
    print("Starting validation...")
    validate_job_ids(german_jobs)
    validate_required_columns(german_jobs)
    validate_blank_values(german_jobs)

    # STEP 4: Prepare
    prepared_jobs = prepare_data(german_jobs)

    # STEP 5: Load
    print("Starting database load...")
    connection = connect_database()

    try:
        load_data(prepared_jobs, connection)
    finally:
        connection.close()

    print("ETL pipeline completed successfully!")


if __name__ == "__main__":
    run_pipeline()
