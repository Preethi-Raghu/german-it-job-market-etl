from pathlib import Path
import pandas as pd

def extract_data(file_path):
    df = pd.read_csv(file_path)
    return df

if __name__ == "__main__":
    project_folder = Path(__file__).resolve().parent.parent
    csv_path = project_folder / "german_jobs.csv"

    df = extract_data(csv_path)

    print("Extraction successful!")
    print("Dataset shape:", df.shape)
    print(df.head())