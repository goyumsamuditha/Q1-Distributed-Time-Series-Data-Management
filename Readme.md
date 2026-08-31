# Distributed Time-Series Data Management with InfluxDB

## Project Overview
This repository contains a complete, automated pipeline for managing, storing, and analyzing large-scale time-series data. Developed as an academic project for distributed data management, it leverages **InfluxDB** to process a historical dataset containing weather observations from Szeged, Hungary, for the year 2006. 

The architecture demonstrates high-throughput batch ingestion, modular Python scripting, native time-series analytics using Flux, and automated data lifecycle management through strict retention policies.

## Technology Stack
*   **Database Engine:** InfluxDB v2 (Time-Series Database)
*   **Infrastructure:** Docker & Docker Compose
*   **Core Language:** Python 3
*   **Database Client:** `influxdb-client` (Python SDK)
*   **Testing & Environment:** `pytest`, `python-dotenv`
*   **Query Language:** Flux

## Repository Structure and File Modularity
The codebase is separated into distinct, specialized modules to ensure maintainability and clean architecture.

### 1. Infrastructure and Configuration
*   **`docker-compose.yml`**: Provisions the InfluxDB container and securely injects initial environment variables (admin credentials, default organization, and primary bucket).
*   **`src/config.py`**: Centralizes secure environment variables for the Python scripts, loading the InfluxDB URL, authentication token, organization name, and bucket name[cite: 4].

### 2. Data Preparation and Ingestion Pipeline
*   **`src/downloader.py`**: Automates the retrieval of the raw CSV datasets using the Kaggle API.
*   **`src/parser.py`**: Cleans the raw CSV data and standardizes the complex 2006 timestamps into a format compatible with time-series databases.
*   **`src/line_protocol.py`**: A dedicated mapping module that converts the parsed Python dictionaries strictly into the InfluxDB Line Protocol format.
*   **`src/ingest.py`**: The master ingestion script. To optimize memory usage and maintain high throughput, it coordinates the parser modules and executes database writes in optimized batches of 5,000 records.

### 3. Analytics and Automation
*   **`flux/window_aggregation.flux`**: A query that calculates sliding hourly temperature averages to smooth out minor data fluctuations[cite: 3].
*   **`flux/anomaly_detection.flux`**: An analytical query containing anomaly isolation filters that capture observations exceeding two standard deviations from the dataset mean[cite: 1].
*   **`flux/downsampling_task.flux`**: A task query that continuously summarizes historical data into an auxiliary 30-day retention bucket to optimize long-term storage[cite: 2].
*   **`src/automate_queries.py`**: The final automation script that utilizes the InfluxDB Python SDK to programmatically execute the external Flux queries, manage bucket retention policies, and register scheduled background tasks without manual UI interaction.

---

## Setup and Execution Guide

### Phase 1: Environment Initialization
1.  **Start the Database Container:**
    Deploy the InfluxDB environment using Docker.
    ```bash
    docker compose up -d
    ```
2.  **Install Python Dependencies:**
    Initialize a virtual environment and install the required packages.
    ```bash
    pip install -r requirements.txt
    ```

### Phase 2: Pipeline Execution
Run the following commands sequentially from the root directory to execute the complete data pipeline.

1.  **Validate Data Logic (Unit Testing):**
    Ensure the parsing and Line Protocol formatting functions operate correctly before interacting with the database.
    ```bash
    python -m pytest tests/
    ```

2.  **Fetch the Dataset:**
    Download the raw historical weather data into the local `data/raw/` directory.
    ```bash
    python src/downloader.py
    ```

3.  **Execute High-Throughput Ingestion:**
    Parse, format, and upload the data. The terminal will output the progress of the batch writes until all 96,453 historical records are successfully committed to the database.
    ```bash
    python src/ingest.py data/raw/weatherHistory.csv
    ```

4.  **Automate Analytics and Lifecycle Policies:**
    Run the master automation script to finalize the database architecture.
    ```bash
    python src/automate_queries.py
    ```
    *Note on execution: This script automatically provisions a new `weather_downsampled` bucket with a strict 30-day retention rule. It then attempts to backfill the 2006 data into this bucket. Because the dataset is twenty years old, InfluxDB will actively reject the write. The script is designed to catch this specific retention exception and log it as a successful validation of the automated lifecycle policy.*

### Phase 3: Data Visualization
To visually verify the ingested data and analytical queries:
1. Navigate to `http://localhost:8086` in your web browser.
2. Authenticate using the credentials defined in the `docker-compose.yml`.
3. Open the **Data Explorer** tab.
4. Set the time range to **Custom (2006-01-01 to 2006-12-31)**.
5. Filter by `_measurement = weather_observations` and `_field = temperature` to render the clean seasonal curve and observe the isolated anomalies.