from sqlmodel import Session, select
from models.tipo import FiltrosTipo, Tipo


class Database_tipos:
    def mostrar_tipos(self, session: Session, filtros: FiltrosTipo) -> list[Tipo]:
        query = self._build_list_query(filtros)
        return session.exec(query).all()

    def cargar_tipos(self, tipos: list[Tipo], session: Session):
        if not session.exec(select(Tipo)).first():
            session.add_all(tipos)
            session.commit()

    def _build_list_query(self, filters: FiltrosTipo):
        query = select(Tipo)
        if filters:
            filtros_dict = filters.model_dump(
                exclude=["limit", "offset"], exclude_none=True
            )
            for key, val in filtros_dict.items():
                if key == "nombre":
                    query = query.where(Tipo.nombre.ilike(f"%{val}%"))
                else:
                    query = query.where(getattr(Tipo, key) == val)

        query = query.limit(filters.limit).offset(filters.offset)
        return query
