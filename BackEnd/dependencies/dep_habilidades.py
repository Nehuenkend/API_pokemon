from typing import Annotated
from fastapi import Depends
from database.db_habilidades import Database_habilidades

database_instance = None


def init_dep_habilidades():
    global database_instance
    database_instance = Database_habilidades()


def get_database() -> Database_habilidades:
    global database_instance
    if database_instance is None:
        raise RuntimeError("Database instance not initialized.")
    return database_instance


DatabaseDep = Annotated[Database_habilidades, Depends(get_database)]
