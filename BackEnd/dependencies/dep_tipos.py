from typing import Annotated
from fastapi import Depends
from database.db_tipos import Database_tipos

database_instance = None


def init_dep_tipos():
    global database_instance
    database_instance = Database_tipos()


def get_database() -> Database_tipos:
    global database_instance
    if database_instance is None:
        raise RuntimeError("Database instance not initialized.")
    return database_instance


DatabaseDep = Annotated[Database_tipos, Depends(get_database)]
