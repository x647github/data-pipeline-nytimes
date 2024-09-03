# Automated ETL Pipeline for New York Times Articles and Bestseller List

This project demonstrates an automated ETL (Extract, Transform, Load) pipeline designed to extract New York Times articles and the current hardcover fiction bestseller list, clean the data, and load it into a PostgreSQL database. The process is fully automated using Apache Airflow.

## Project Structure
- `dags/`: Contains the Airflow DAGs that orchestrate the ETL process.
  - `nyt_articles_etl.py`: DAG for extracting, cleaning, and loading New York Times articles.
  - `nyt_bestsellers_etl.py`: DAG for extracting, cleaning, and loading the New York Times hardcover fiction bestseller list.

- `extract_python_scripts/`: Contains the Python scripts used for the extraction process.
  - `extract_nyt_articles.py`: Script to extract New York Times articles for the current month using the New York Times API.
  - `extract_nyt_bestsellers.py`: Script to extract the current New York Times hardcover fiction bestseller list using the New York Times API.
 
## ETL Process
1. Extraction \
Extracted articles of the current month and hardcover fiction bestseller list using the [New York Times API](https://developer.nytimes.com/).

2. Transformation \
Data is cleaned and processed within the ETL DAGs to ensure it is ready for analysis. This includes handling missing values and filtering unnecessary information.

3. Load \
The cleaned datasets are loaded into a PostgreSQL database using the ETL DAGs.

## Automation with Airflow
The ETL process is orchestrated using Apache Airflow, which handles scheduling, monitoring, and managing the entire pipeline. \
The ETL DAGs located in the `dags/` directory control the sequence of operations for the pipeline.
