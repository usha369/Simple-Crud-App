import mariadb
import os
from dotenv import load_dotenv
load_dotenv()

def get_connection():
    try:
        conn = mariadb.connect(
            user = os.getenv('DB_USER'),
            password = os.getenv('DB_PASSWORD'),
            host = os.getenv('DB_HOST'),
            port = 3306,
            database = os.getenv('DB_NAME')
        )
        return conn
    except Exception as e:
        print(f"Unable to connect database: {e}")


