import os
from dotenv import load_dotenv

load_dotenv()


def get_postgress_uri():
    host = os.environ.get("DB_HOST", "localhost")
    port = 5432 if host == "localhost" else 5432
    password = os.environ.get("DB_PASSWORD", "abc123")
    user, db_name = os.environ.get("DB_USERNAME", "localhost"), os.environ.get("DB_NAME", "localhost")
    return f"postgresql://{user}:{password}@{host}:{port}/{db_name}"


def get_api_url():
    host = os.environ.get("API_HOST", "localhost")
    port = 5000 if host == "localhost" else 80
    return f"http://{host}:{port}"