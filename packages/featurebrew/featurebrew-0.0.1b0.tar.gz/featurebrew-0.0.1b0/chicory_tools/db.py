import os
from typing import Annotated, Any

from langchain_core.tools import tool
from sqlalchemy.dialects.postgresql import psycopg2


class DBClient:
    def __init__(self):
        host = os.environ.get("DB_HOST", '')
        user = os.environ.get("DB_USER", '')
        password = os.environ.get("DB_PASS", '')
        database = os.environ.get("DB_NAME", '')
        self.client = psycopg2.connect(host=host, port=5439, user=user, password=password, database=database)


    def run_query(self, query: Annotated[str, "SQL Query to be run against the database"]) -> list[tuple[Any, ...]]:
        with self.client.cursor() as cursor:
            try:
                cursor.execute(query)
                results = cursor.fetchall()
                return results
            except Exception as e:
                print(e)
                return str(e)

@tool
def db_client(query):
    """Get the db client (psycopg2) response for passed query formatted as a string."""
    db_client = DBClient()
    return db_client(query)