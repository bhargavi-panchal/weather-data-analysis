# Weather API Data Analysis Project

## Project Overview
This project demonstrates an end-to-end data engineering pipeline that ingests real-time weather data from a public Weather API, processes it using Python, stores raw data in Amazon S3, transforms it using AWS Glue, and finally loads curated data into Amazon Redshift for analytics.
The entire workflow is orchestrated using Apache Airflow and it uses AWS Code Build for CI/CD pipeline for code commits and automated builds, showcasing production-style scheduling and dependency management.

## Tech Stack

- Cloud Platform: AWS
- API - https://openweathermap.org/forecast5
- Storage: Amazon S3
- Programming Language: Python
- Libraries:
  - requests – API data extraction
  - pandas – data processing
- ETL: AWS Glue
- Data Warehouse: Amazon Redshift
- Automation: AWS Code Build
- Orchestration: Apache Airflow


## Architecture Overview and Workflow

![Project_Architecture](architecture.png)

The project workflow is designed to automate the extraction, processing, and storage of weather data efficiently:

1. **Development and CI/CD:**
- Code is developed locally on the **dev branch** in **Visual Studio Code**.
- Changes are committed and pushed to the **remote dev branch** via **AWS CodeBuild**, which uses `buildspec.yml` to:
- Copy DAG files to the S3 Airflow bucket.
- Copy `requirements.txt` to S3.
- Copy Glue scripts to the S3 scripts folder.
- A **pull request (PR)** is created to merge changes from **remote dev** to **remote main**.


2. **Airflow Jobs:**
- **Scheduling:** Airflow jobs run daily, with code stored in the `dags` folder of the managed Airflow S3 bucket: `s3://weather-airflow-managed-gds/dags/`.
- **Job 1 (Data Extraction):**
- Triggered automatically according to schedule.
- Fetches data from the public weather API endpoint: `https://api.openweathermap.org/data/2.5/forecast`.
- Stores extracted data as raw CSV files in Hive-style partitions (e.g., `date=2026-01-27/`) in the S3 bucket: `s3://weather-data-project-gds`.
- **Job 2 (Data Processing):**
- Triggered after Job 1 completes.
- Initiates an **AWS Glue Job**, with scripts stored in: `s3://aws-glue-assets/scripts/`.
- Reads raw weather data from S3.
- Writes curated weather data into **Amazon Redshift** tables.


    
## Features
- Daily automated data extraction from a public weather API.
- Process and clean raw data in CSV format.
- Store raw and curated data in AWS S3 and Amazon Redshift.
- Schedule and orchestrate workflows using Apache Airflow.
- CI/CD pipeline with AWS CodeBuild and Git for version-controlled deployments.

## Credits
This project is based on a tutorial by [Shashank Mishra](https://www.growdataskills.com/course-aws-data-engineering)

