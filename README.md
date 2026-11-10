
# German IT Job Market ETL Pipeline

A Python ETL pipeline that extracts German job postings, filters and cleans the IT-related ones, validates the data, and loads it into Microsoft SQL Server for analysis.

**Question this project answers:** Where in Germany are IT jobs posted, and what do they look like?

## Pipeline Architecture

```
Parquet → CSV → Extract → Transform → Validate → Load → SQL Server
```

| Step | File | What it does |
|------|------|--------------|
| Extract | `src/extract.py` | Reads the CSV into a pandas DataFrame |
| Transform | `src/transform.py` | Filters IT jobs (English and German keywords), cleans and standardizes data, filters German regions |
| Validate | `src/validate.py` | Checks for duplicate or missing job IDs, required columns, and blank values |
| Load | `src/load.py` | Connects to SQL Server and inserts rows, preventing duplicate inserts |
| Orchestrate | `src/pipeline.py` | Runs all steps in order |

## Data Source

**German Job Postings (Stellen-Atlas)** by mischeiwiller, hosted on Hugging Face:
https://huggingface.co/datasets/mischeiwiller/german-job-postings

- 70,584 real job postings, in Parquet format
- Includes titles, employers, regions, posting dates, seniority, and machine-generated occupation and skill classifications
- License: CC BY 4.0 (attribution required)

## Results

- **70,584** source records processed
- **1,038** IT job records loaded into SQL Server after filtering and cleaning

Top regions by number of IT postings:

| Rank | Region | Postings |
|------|--------|----------|
| 1 | Nordrhein-Westfalen | 236 |
| 2 | Bayern | 154 |
| 3 | Sachsen | 116 |
| 4 | Bremen | 101 |
| 4 | Berlin | 101 |
| 6 | Baden-Württemberg | 96 |
| 7 | Hamburg | 76 |
| 8 | Hessen | 67 |
| 9 | Niedersachsen | 57 |
| 10 | Schleswig-Holstein | 15 |


## Tech Stack

Python, pandas, pyodbc, pyarrow, Microsoft SQL Server Express, Git

## Setup

**Requirements:** Python 3.10+, SQL Server Express, and [ODBC Driver 18 for SQL Server](https://learn.microsoft.com/en-us/sql/connect/odbc/download-odbc-driver-for-sql-server)

1. Clone the repo and install dependencies:
   ```bash
   git clone https://github.com/Preethi-Raghu/german-it-job-market-etl.git
   cd german-it-job-market-etl
   pip install -r requirements.txt
   ```
2. Download the dataset (`german-job-postings.parquet`) from Hugging Face and convert it to CSV:
   ```bash
   python scripts/parquet_to_csv.py
   ```
3. Create a database named `GermanITJobMarket` and a table `dbo.JobPostings` in SQL Server Express. 

4. Run the pipeline:
   ```bash
   python src/pipeline.py
   ```

The connection uses Windows authentication to `.\SQLEXPRESS`. Change the server name in `src/load.py` if your setup differs.

## Project Structure

```
├── src/          # extract, transform, validate, load, pipeline
├── scripts/      # helper scripts (data exploration, parquet to CSV)
├── requirements.txt
└── README.md
```

## Roadmap

- [ ] Unit tests with pytest and CI via GitHub Actions
- [ ] SQL analysis queries (window functions, CTEs)
- [ ] Docker Compose setup
- [ ] Airflow DAG for scheduling
- [ ] Logging instead of print statements

## Credits

Dataset: *German Job Postings (Stellen-Atlas)* by mischeiwiller, licensed under [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/).