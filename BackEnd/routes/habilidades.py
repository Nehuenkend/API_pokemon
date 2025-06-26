from typing import Annotated, List
from fastapi import APIRouter, Query
from dependencies.sql import SessionDep

from dependencies.dep_habilidades import DatabaseDep
from models.habilidad import FiltrosHabilidad, Habilidad

router = APIRouter()


@router.get("/", response_model=List[Habilidad])
def habilidades(
    db: DatabaseDep, session: SessionDep, filtros: Annotated[FiltrosHabilidad, Query()]
):
    return db.mostrar_habilidades(session, filtros)
