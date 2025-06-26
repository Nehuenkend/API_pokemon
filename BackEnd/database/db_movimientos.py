from fastapi import HTTPException

from sqlmodel import Session, select
from models.movimiento import (
    FiltrosMovimiento,
    Movimiento,
)


class Database_movimientos:

    def cargar_movimientos(self, movimientos: list[Movimiento], session: Session):
        if not session.exec(select(Movimiento)).first():
            session.add_all(movimientos)
            session.commit()

    def mostrar_movimientos(
        self, session: Session, filtros: FiltrosMovimiento
    ) -> list[Movimiento]:
        query = self._build_list_query(filtros)
        movimientos = session.exec(query).all()
        return movimientos

    def obtener_movimiento(self, session: Session, id_movimiento: int) -> Movimiento:
        mov = session.exec(
            select(Movimiento).where(Movimiento.id == id_movimiento)
        ).first()
        if not mov:
            raise HTTPException(status_code=404, detail="Movimiento not found")
        return mov

    def _build_list_query(self, filters: FiltrosMovimiento):
        query = select(Movimiento)
        if filters:
            filtros_dict = filters.model_dump(
                exclude=["limit", "offset"], exclude_none=True
            )
            for key, val in filtros_dict.items():
                if key == "nombre":
                    query = query.where(Movimiento.nombre.ilike(f"%{val}%"))
                elif key == "tipo":
                    query = query.where(Movimiento.tipos.contains([{"id": val}]))
                else:
                    query = query.where(getattr(Movimiento, key) == val)

        query = query.limit(filters.limit).offset(filters.offset)
        return query
