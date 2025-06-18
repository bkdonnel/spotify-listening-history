import snowflake.connector
from cryptography.hazmat.primitives import serialization

# Path to your unencrypted private key file (PEM format)
PRIVATE_KEY_PATH = "/Users/bryandonnelly/Documents/GitHub/spotify-listening-history/streamlit/secrets/rsa_key.pem"

# Snowflake connection parameters
USER = "spotify_service_user"
ACCOUNT = "mtxrhhc-ti99989"
WAREHOUSE = "COMPUTE_WH"
DATABASE = "spotify"
SCHEMA = "raw"

def main():
    print("Starting connection test...")
    # Load your private key and convert to DER format bytes
    with open(PRIVATE_KEY_PATH, "rb") as key_file:
        private_key_obj = serialization.load_pem_private_key(
            key_file.read(),
            password=None,
        )
        private_key = private_key_obj.private_bytes(
            encoding=serialization.Encoding.DER,
            format=serialization.PrivateFormat.PKCS8,
            encryption_algorithm=serialization.NoEncryption()
        )
    print("Private key loaded.")

    # Connect to Snowflake using key-pair auth
    ctx = snowflake.connector.connect(
        user=USER,
        account=ACCOUNT,
        private_key=private_key,
        warehouse=WAREHOUSE,
        database=DATABASE,
        schema=SCHEMA
    )
    print("Connected to Snowflake!")

    cs = ctx.cursor()
    try:
        cs.execute("SELECT CURRENT_VERSION()")
        one_row = cs.fetchone()
        print(f"Snowflake version: {one_row[0]}")
    finally:
        cs.close()
        ctx.close()
    print("Connection closed.")

if __name__ == "__main__":
    main()
