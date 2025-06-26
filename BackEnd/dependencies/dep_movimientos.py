from database.db_movimientos import Database_movimientos
from typing import Annotated
from fastapi import Depends

__database_instance = None


def init_dep_movimientos():
    global __database_instance
    __database_instance = Database_movimientos()


def get_database() -> Database_movimientos:
    global __database_instance
    if __database_instance is None:
        raise RuntimeError("Database instance not initialized.")
    return __database_instance


DatabaseDepMovimientos = Annotated[Database_movimientos, Depends(get_database)]
