
from pathlib import Path


# Function 1: Validate job IDs
def validate_job_ids(df):

    duplicate_count = df["id"].duplicated().sum()
    missing_count = df["id"].isnull().sum()

    if duplicate_count > 0:
        raise ValueError(
            f"Found {duplicate_count} duplicate job IDs!"
        )

    if missing_count > 0:
        raise ValueError(
            f"Found {missing_count} missing job IDs!"
        )

    print("Job ID validation passed!")


# Function 2: Validate required columns
def validate_required_columns(df):

    required_columns = [
        "id",
        "title",
        "region",
        "posted_date"
    ]

    missing_count = df[required_columns].isnull().sum().sum()

    if missing_count > 0:
        raise ValueError(
            f"Found {missing_count} missing required values!"
        )

    print("Required columns validation passed!")


# Function 3: Validate blank values
def validate_blank_values(df):

    required_text_columns = ["id", "title", "region"]

    for column in required_text_columns:

        blank_count = (
            df[column].astype("string").str.strip().eq("")
        ).sum()

        if blank_count > 0:
            raise ValueError(
                f"Found {blank_count} blank values in {column}!"
            )

    print("Blank value validation passed!")


# Testing section
if __name__ == "__main__":

    from extract import extract_data
    from transform import (
        filter_it_jobs,
        clean_job_data,
        filter_german_regions
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

    print("Total validated records:", len(german_jobs))
