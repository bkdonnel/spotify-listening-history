from pathlib import Path
import os
from snowflake.sqlalchemy import URL
from sqlalchemy import create_engine
from cryptography.hazmat.primitives import serialization

def get_engine():
    user = os.getenv("SNOWFLAKE_USER")
    account = os.getenv("SNOWFLAKE_ACCOUNT")
    database = os.getenv("SNOWFLAKE_DATABASE")
    schema = os.getenv("SNOWFLAKE_SCHEMA")
    warehouse = os.getenv("SNOWFLAKE_WAREHOUSE")
    role = os.getenv("SNOWFLAKE_ROLE")
    private_key_path = os.getenv("SNOWFLAKE_PRIVATE_KEY_PATH")

    if not private_key_path or not Path(private_key_path).exists():
        raise FileNotFoundError(f"Private key file not found at {private_key_path}")

    with open(private_key_path, "rb") as key_file:
        private_key_obj = serialization.load_der_private_key(
            key_file.read(),
            password=None,
        )

    private_key_bytes = private_key_obj.private_bytes(
        encoding=serialization.Encoding.DER,
        format=serialization.PrivateFormat.PKCS8,
        encryption_algorithm=serialization.NoEncryption()
    )

    engine = create_engine(
        URL(
            user=user,
            account=account,
            database=database,
            schema=schema,
            warehouse=warehouse,
            role=role,
        ),
        connect_args={"private_key": private_key_bytes}
    )

    return engine
