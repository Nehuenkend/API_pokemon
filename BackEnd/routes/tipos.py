from typing import Annotated, List
from fastapi import APIRouter, Query
from dependencies.sql import SessionDep
from models.tipo import FiltrosTipo, Tipo
from dependencies.dep_tipos import DatabaseDep

router = APIRouter()


@router.get("/", response_model=List[Tipo])
def tipos(
    db: DatabaseDep, session: SessionDep, filtros: Annotated[FiltrosTipo, Query()]
):
    return db.mostrar_tipos(session, filtros)
