
import pandas as pd
from pathlib import Path


# STEP 1: Filter IT jobs
def filter_it_jobs(df):

    job_keywords = [
        "data engineer",
        "data analyst",
        "software developer",
        "softwareentwickler",
        "cloud engineer",
        "devops",
        "dateningenieur"
    ]

    pattern = "|".join(job_keywords)

    it_jobs = df[
        df["title"].str.contains(
            pattern,
            case=False,
            na=False
        )
    ].copy()

    return it_jobs


# STEP 2: Clean job data
def clean_job_data(it_jobs):

    cleaned_jobs = it_jobs.copy()

    # Remove unnecessary column
    cleaned_jobs = cleaned_jobs.drop(
        columns=["description_derived"]
    )

    # Handle missing regions
    cleaned_jobs["region"] = (
        cleaned_jobs["region"].fillna("unknown")
    )

    # Convert dates
    cleaned_jobs["posted_date"] = pd.to_datetime(
        cleaned_jobs["posted_date"],
        errors="coerce"
    )

    cleaned_jobs["fetched_at"] = pd.to_datetime(
        cleaned_jobs["fetched_at"],
        errors="coerce",
        utc=True
    )

    # Clean text columns
    cleaned_jobs["title"] = (
        cleaned_jobs["title"].str.strip()
    )

    cleaned_jobs["region"] = (
        cleaned_jobs["region"].str.strip()
    )

    cleaned_jobs["seniority"] = (
        cleaned_jobs["seniority"].str.strip().str.lower()
    )

    return cleaned_jobs


# STEP 3: Filter German regions
def filter_german_regions(cleaned_jobs):

    german_regions = [
        "Baden-Württemberg",
        "Bayern",
        "Berlin",
        "Brandenburg",
        "Bremen",
        "Hamburg",
        "Hessen",
        "Mecklenburg-Vorpommern",
        "Niedersachsen",
        "Nordrhein-Westfalen",
        "Rheinland-Pfalz",
        "Saarland",
        "Sachsen",
        "Sachsen-Anhalt",
        "Schleswig-Holstein",
        "Thüringen"
    ]

    german_jobs = cleaned_jobs[
        cleaned_jobs["region"].isin(german_regions)
    ].copy()

    # Convert KLDB codes to strings
    german_jobs["kldb_2010"] = (
        german_jobs["kldb_2010"]
        .astype("Int64")
        .astype("string")
    )

    return german_jobs


# TESTING SECTION
if __name__ == "__main__":

    from extract import extract_data

    project_folder = Path(__file__).resolve().parent.parent
    csv_path = project_folder / "german_jobs.csv"

    # Extract
    df = extract_data(csv_path)

    # Transform
    it_jobs = filter_it_jobs(df)
    cleaned_jobs = clean_job_data(it_jobs)
    german_jobs = filter_german_regions(cleaned_jobs)

    # Display results
    print("Original records:", len(df))
    print("Filtered IT jobs:", len(it_jobs))
    print("German IT jobs:", len(german_jobs))
    print("Final dataset shape:", german_jobs.shape)

    print("\nDate column types:")
    print(german_jobs[["posted_date", "fetched_at"]].dtypes)

    print("\nKLDB data type:")
    print(german_jobs["kldb_2010"].dtype)
