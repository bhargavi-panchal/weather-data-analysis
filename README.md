# Weather API Data Analysis Project

## Project Overview
This project demonstrates an end-to-end data engineering pipeline that ingests real-time weather data from a public Weather API, processes it using Python, stores raw data in Amazon S3, transforms it using AWS Glue, and finally loads curated data into Amazon Redshift for analytics.
The entire workflow is orchestrated using Apache Airflow and it uses AWS Code Build for CI/CD pipeline for code commits and automated builds, showcasing production-style scheduling and dependency management.

## Architecture Overview

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

    
## Features
- Fetch weather data from an external API.
- Process and clean JSON and CSV data formats.
- Store data in AWS S3 for archival.
- Analyze trends and generate visualizations.
- Automated deployment and version control using Git and AWS CodeBuild.

## Architecture
The workflow is as follows:
1. Code is developed locally on the **dev branch** in **Visual Studio Code**.
2. Changes are committed to the **remote dev branch** using **AWS CodeBuild**.
3. A **pull request (PR)** is created in Git to merge changes from **remote dev** to **remote main**.
4. Weather data is fetched via the API and processed using **Python / PySpark** scripts.
5. Cleaned data is stored in **S3 buckets**.
6. Analytics and visualizations are generated from the stored data.
7. Optional: Reports and dashboards can be hosted using **AWS QuickSight** or exported as files.

### AWS Services Used
- **S3:** Data storage for raw and processed data.
- **CodeBuild:** CI/CD pipeline for code commits and automated builds.
- **Lambda / EC2 (if applicable):** Running analysis scripts.
- **QuickSight (optional):** Visualization dashboards.

