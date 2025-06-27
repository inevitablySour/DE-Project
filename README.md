# Health Data Engineering Project

This project involves extracting, cleaning, loading, and querying healthcare data using PostgreSQL and Python.

## Data Loading Structure

DE-Project/
├── cleaned_data/            # All cleaned CSV files go here
├── docker-compose.yml       # Sets up PostgreSQL with volume
├── init.sql                 # Creates tables in PostgreSQL
├── load_data.py           # Loads CSV data into the DB
├── queries.py           # Runs 5 SQL queries and saves results
├── output/                  # Query output CSVs will appear here
└── README.md                # This file

## Prerequisites

Make sure you have the following installed:

- Docker: https://docs.docker.com/get-docker/
- Python 3.9+ : https://www.python.org/downloads/
- Git

Then install Python packages:

pip install pandas sqlalchemy psycopg2-binary pyarrow

## Setup Instructions

1. Clone the repository

git clone https://github.com/your-org/your-repo.git
cd your-repo

2. Place cleaned CSVs in the `cleaned_data/` folder

Make sure the folder contains:
- patients_cleaned.csv
- encounters_cleaned.csv
- observations_cleaned.csv
- diagnoses_cleaned.csv
- procedures_cleaned.csv
- medications_cleaned.csv

3. Start the PostgreSQL container

docker-compose up

This will:
- Start a PostgreSQL container on port 5432
- Automatically create the database and schema from `init.sql`

4. Import the data into PostgreSQL

python load_data.py

5. Run the project queries

python queries.py

Query results will be saved as CSV files in the `output/` folder.

## Queries Included

- Q1: Average age and age range of patients
- Q2: Average number of patients per physician
- Q3: Most common diagnoses by age group
- Q4: Medications prescribed per diagnosis
- Q5: Average number of procedures per encounter

## Notes

If your database breaks, stop Docker (CTRL+C) and run:

docker-compose down -v
docker-compose up
