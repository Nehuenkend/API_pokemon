from database.db_generaciones import Database_generaciones
from typing import Annotated
from fastapi import Depends

__database_instance = None


def init_dep_generaciones():
    global __database_instance
    __database_instance = Database_generaciones()


def get_database() -> Database_generaciones:
    global __database_instance
    if __database_instance is None:
        raise RuntimeError("Database instance not initialized.")
    return __database_instance


DatabaseDepGeneraciones = Annotated[Database_generaciones, Depends(get_database)]
