#Data Exploration
from pathlib import Path
import pandas as pd

folder = Path(__file__).resolve().parent

file_path = folder / "german_jobs.csv"

df = pd.read_csv(file_path)

print("CSV loaded successfully!")
print(df.shape)
print(df.head())
print("Dataset shape:\n",df.shape)
print("dataset columns:\n",df.columns)
print("data types:\n",df.dtypes)
print("missing values:\n",df.isnull().sum())
print("duplicate rows:\n",df.duplicated().sum())

print("seniority levels:\n",df["seniority"].value_counts(dropna=False))
print(df["esco_skills"].head(10).to_list())

#filtering 
jobs = [
    "data engineer",
    "data analyst",
    "software developer",
    "softwareentwickler",
    "cloud engineer",
    "devops",
    "dateningenieur"
]
pattern = '|'.join(jobs)
it_jobs=df[df['title'].str.contains(pattern,case=False,na=False)]
print(it_jobs['title'].head(20))
print('total IT jobs:',len(it_jobs))


print(it_jobs.isnull().sum())
print(it_jobs.duplicated().sum())
print("seniority_count:", it_jobs["seniority"].value_counts(dropna=False))
print("region_count:", it_jobs["region"].value_counts().head(10))

# tranformation 

cleaned_jobs=it_jobs.copy()
cleaned_jobs=cleaned_jobs.drop(columns=['description_derived'])

cleaned_jobs['region']=cleaned_jobs['region'].fillna('unknown')

print('cleaned_jobs shape:', cleaned_jobs.shape)
print('cleaned_jobs missing values:\n', cleaned_jobs.isnull().sum())    

cleaned_jobs["posted_date"] = pd.to_datetime(
    cleaned_jobs["posted_date"],
    errors="coerce")

cleaned_jobs['fetched_at']=pd.to_datetime(cleaned_jobs['fetched_at'],errors='coerce')

print(cleaned_jobs[["posted_date", "fetched_at"]].dtypes)

print(cleaned_jobs[["posted_date", "fetched_at"]].isnull().sum())

cleaned_jobs['region']=cleaned_jobs['region'].str.strip()
cleaned_jobs['seniority']=cleaned_jobs['seniority'].str.strip()

print(cleaned_jobs['region'].value_counts())
print(cleaned_jobs['seniority'].value_counts())
print(cleaned_jobs[["title", "region", "seniority"]].head())

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

print(cleaned_jobs["region"].isin(german_regions).value_counts())

german_jobs=cleaned_jobs[cleaned_jobs['region'].isin(german_regions)].copy()
german_jobs["kldb_2010"] = (
    german_jobs["kldb_2010"]
    .astype("Int64")
    .astype("string")
)

print(german_jobs["kldb_2010"].head(10))
print("Data type:", german_jobs["kldb_2010"].dtype)
print("Missing values:", german_jobs["kldb_2010"].isnull().sum())
print("Before filtering:", cleaned_jobs.shape)
print("After filtering:", german_jobs.shape)

print(german_jobs["region"].value_counts())

#DATA VALIDATION
print("Total records:", len(german_jobs))

print("Duplicate job IDs:", german_jobs["id"].duplicated().sum())

print("Missing job IDs:", german_jobs["id"].isnull().sum())

important_columns = ["id", "title", "region", "posted_date"]

print(german_jobs[important_columns].isnull().sum())

today = pd.Timestamp.today().normalize()

future_jobs = german_jobs[
    german_jobs["posted_date"] > today
]

print("Future-dated jobs:", len(future_jobs))

print("Earliest posting:", german_jobs["posted_date"].min())

print("Latest posting:", german_jobs["posted_date"].max())

german_jobs["title"].str.strip().eq("")

print("Blank job titles:",
      german_jobs["title"].str.strip().eq("").sum())

print("Blank regions:",
      german_jobs["region"].str.strip().eq("").sum())

print("Blank employers:",
      german_jobs["employer"].str.strip().eq("").sum())

def check_duplicate_ids(df):
    duplicate_count = df["id"].duplicated().sum()
    return duplicate_count

result = check_duplicate_ids(german_jobs)
print("Duplicate IDs:", result)

def check_missing_ids(df):
    missing_count = df["id"].isnull().sum()
    return missing_count

result = check_missing_ids(german_jobs)
print("Missing IDs:", result)

def validate_job_ids(df):
    duplicate_count = df["id"].duplicated().sum()
    missing_count = df["id"].isnull().sum()

    if duplicate_count > 0:
        raise ValueError("Duplicate job IDs found!")

    if missing_count > 0:
        raise ValueError("Missing job IDs found!")

    print("Job ID validation passed")


#testing 1
# test_jobs = pd.DataFrame({
#     "id": [101, None, 103]
# })

# print(test_jobs)
# validate_job_ids(test_jobs)

# validate_job_ids(test_jobs)

# test_jobs = pd.DataFrame({
#     "id": [101, None, 103]
# })

# validate_job_ids(test_jobs)

# test_jobs = pd.DataFrame({
#     "id": [101, 102, 103]
# })

# validate_job_ids(test_jobs)

# testing 2
test_jobs = pd.DataFrame({
    "id": [101, 102, 103]
})

validate_job_ids(test_jobs)


def validate_required_columns(df):
    required_columns = ["id", "title", "region", "posted_date"]

    missing_count = df[required_columns].isnull().sum().sum()

    if missing_count > 0:
        raise ValueError("Missing values in required columns!")

    print("Required columns validation passed")

validate_job_ids(german_jobs)
validate_required_columns(german_jobs)

# test_jobs = pd.DataFrame({
#     "id": [101, 102, 103],
#     "title": ["Data Engineer", None, "Data Analyst"],
#     "region": ["Berlin", "Bayern", "Hamburg"],
#     "posted_date": ["2026-01-10", "2026-02-15", "2026-03-20"]
# })

# validate_required_columns(test_jobs)

print(german_jobs.dtypes)


print("ID examples:")
print(german_jobs["id"].head(5).to_list())

print("\nKLDB examples:")
print(german_jobs["kldb_2010"].head(10).to_list())

print("\nESCO skills example:")
print(german_jobs["esco_skills"].iloc[0])

print("\nSalary examples:")
print(german_jobs["salary_range"].dropna().head(5).to_list())

text_columns = german_jobs.select_dtypes(include=["object"]).columns

for col in text_columns:
    max_length = german_jobs[col].dropna().astype(str).str.len().max()
    print(f"{col}: {max_length}")

load_jobs = german_jobs.copy()

load_jobs = load_jobs.astype(object).where(
    pd.notna(load_jobs),
    None
)

print("Original missing salary values:",
      german_jobs["salary_range"].isnull().sum())

print("SQL-ready missing salary values:",
      load_jobs["salary_range"].apply(lambda x: x is None).sum())

print("Total records:", len(load_jobs))

load_jobs["posted_date"] = load_jobs["posted_date"].apply(
    lambda x: x.date() if x is not None else None
)

print(load_jobs["posted_date"].head())

print("Python type:",
      type(load_jobs["posted_date"].iloc[0]))

print(load_jobs["fetched_at"].head())

print("Python type:",
      type(load_jobs["fetched_at"].iloc[0]))

print("Timezone:",
      load_jobs["fetched_at"].iloc[0].tzinfo)

load_jobs["fetched_at"] = load_jobs["fetched_at"].apply(
    lambda x: x.isoformat() if x is not None else None
)

print(load_jobs["fetched_at"].head())

print("Python type:",
      type(load_jobs["fetched_at"].iloc[0]))

test_row = load_jobs.iloc[0]

print(test_row)

print(load_jobs.columns.tolist())

for column in load_jobs.columns:
    print(column, type(test_row[column]))

load_jobs.to_pickle("prepared_jobs.pkl")