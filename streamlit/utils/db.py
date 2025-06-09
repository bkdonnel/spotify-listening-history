from sqlalchemy import create_engine
import os

def get_engine():
    user = os.getenv("SNOWFLAKE_USER")
    password = os.getenv("SNOWFLAKE_PASSWORD")
    account = os.getenv("SNOWFLAKE_ACCOUNT")
    database = os.getenv("SNOWFLAKE_DATABASE")
    schema = os.getenv("SNOWFLAKE_SCHEMA")
    warehouse = os.getenv("SNOWFLAKE_WAREHOUSE")

    conn_str = f"snowflake://{user}:{password}@{account}/{database}/{schema}?warehouse={warehouse}"
    return create_engine(conn_str)
