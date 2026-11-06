import pandas as pd

df = pd.read_parquet("german-job-postings.parquet")

df.to_csv("german_jobs.csv", index=False)

print("CSV file created successfully!")