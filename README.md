# Spotify Listening History ETL & Dashboard

Project that extracts your Spotify listening history, loads it into Snowflake via Airflow, transforms it with dbt, and visualizes it in a Streamlit dashboard — all containerized using Docker.

## Project Overview

This project demonstrates an end-to-end modern data stack using:

- **Airflow** – for orchestration and scheduling ETL jobs.
- **dbt** – for transforming raw Spotify data into analytics-ready models.
- **Snowflake** – cloud data warehouse for storage and querying.
- **Streamlit** – interactive dashboard to explore your listening habits.
- **Docker** – for containerized deployment of all services.

![Screenshot](images/Screenshot 2025-06-18 at 2.32.35 PM.png)
---

## Features

- OAuth with Spotify to collect recent listening data.
- Airflow DAG that:
  - Extracts data using Spotify's Web API
  - Loads raw data into Snowflake
  - Triggers dbt models to transform data
- dbt models include staging and analytics layers
- Streamlit dashboard to visualize your top tracks, artists, and trends

---

## Architecture

```text
User → Spotify API → Airflow (ETL) → Snowflake (raw → analytics via dbt) → Streamlit (dashboard)
