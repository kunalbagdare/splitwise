import os

def create_connection_string():
    """
    The function `create_connection_string` creates a connection string for a PostgreSQL database using
    environment variables, and falls back to a SQLite database if the environment variables are not set.
    """
    try:
        PG_USER = os.getenv("POSTGRES_USER")
        PG_PASSWORD = os.getenv("POSTGRES_PASSWORD")
        PG_HOST = os.getenv("POSTGRES_HOST", "localhost")
        PG_DB = os.getenv("POSTGRES_DB", "splitwise")
        PG_PORT = os.getenv("POSTGRES_PORT", 5432)
        return f"postgresql+psycopg2://{PG_USER}:{PG_PASSWORD}@{PG_HOST}:{PG_PORT}/{PG_DB}"
    except:
        return "sqlite:///test.db"

MAILGUN_DOMAIN = os.getenv("MAILGUN_DOMAIN")
MAILGUN_API_KEY = os.getenv("MAILGUN_API_KEY")

CELERY_BORKER_URL = os.getenv("CELERY_BORKER_URL","redis://localhost:6379/0")
CELERY_BACKEND_URL = os.getenv("CELERY_BACKEND_URL","redis://localhost:6379/0")