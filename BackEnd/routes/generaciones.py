from typing import List
from fastapi import APIRouter
from dependencies.sql import SessionDep
from models.generacion import Generacion
from dependencies.dep_generaciones import DatabaseDepGeneraciones

router = APIRouter()


@router.get("/", response_model=List[Generacion])
def generaciones(db: DatabaseDepGeneraciones, session: SessionDep):
    return db.mostrar_generaciones(session)
