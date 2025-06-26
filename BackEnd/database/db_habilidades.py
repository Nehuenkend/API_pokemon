from sqlmodel import Session, select
from models.habilidad import FiltrosHabilidad, Habilidad


class Database_habilidades:
    def mostrar_habilidades(
        self, session: Session, filtros: FiltrosHabilidad
    ) -> list[Habilidad]:
        query = self._build_list_query(filtros)
        return session.exec(query).all()

    def cargar_habilidades(self, habilidades: list[Habilidad], session: Session):
        if not session.exec(select(Habilidad)).first():
            session.add_all(habilidades)
            session.commit()

    def _build_list_query(self, filters: FiltrosHabilidad):
        query = select(Habilidad)
        if filters:
            filtros_dict = filters.model_dump(
                exclude=["limit", "offset"], exclude_none=True
            )
            for key, val in filtros_dict.items():
                if key == "nombre":
                    query = query.where(Habilidad.nombre.ilike(f"%{val}%"))
                else:
                    query = query.where(getattr(Habilidad, key) == val)

        query = query.limit(filters.limit).offset(filters.offset)
        return query
