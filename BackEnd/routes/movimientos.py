from typing import Annotated
from fastapi import APIRouter, Query
from dependencies.sql import SessionDep
from dependencies.dep_movimientos import DatabaseDepMovimientos
from models.movimiento import FiltrosMovimiento
from models.public import MovimientoPublicWithRelations, MovimientosPublicWithRelations

router = APIRouter()


@router.get("/")
def movimientos(
    session: SessionDep,
    db: DatabaseDepMovimientos,
    filtros: Annotated[FiltrosMovimiento, Query()],
) -> list[MovimientosPublicWithRelations]:
    return db.mostrar_movimientos(session, filtros)


@router.get("/{id_movimiento}")
def info_movimiento(
    session: SessionDep, db: DatabaseDepMovimientos, id_movimiento: int
) -> MovimientoPublicWithRelations:
    return db.obtener_movimiento(session, id_movimiento)
