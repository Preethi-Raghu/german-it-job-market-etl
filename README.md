
# German IT Job Market ETL Pipeline

A Python-based ETL pipeline that processes German IT job postings and loads cleaned data into Microsoft SQL Server.

## Technologies
- Python
- Pandas
- SQL Server
- pyodbc
- Git

## Pipeline Architecture

CSV → Extract → Transform → Validate → SQL Server

## Features
- Processes 70,584 source records
- Filters relevant IT job postings
- Cleans and standardizes job data
- Validates missing and duplicate values
- Loads 1,038 German IT job records into SQL Server
- Prevents duplicate inserts

## Project Structure

- src/extract.py — Data extraction
- src/transform.py — Data transformation
- src/validate.py — Data validation
- src/load.py — Database loading
- src/pipeline.py — Pipeline orchestration

## Status

Core ETL pipeline completed.
Production improvements planned.
