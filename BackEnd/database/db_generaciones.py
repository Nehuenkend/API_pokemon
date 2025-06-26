from sqlmodel import Session, select
from models.generacion import Generacion, GeneracionBase


class Database_generaciones:
    def mostrar_generaciones(self, session: Session):
        return session.exec(select(Generacion)).all()

    def cargar_generaciones(self, generaciones: list[GeneracionBase], session: Session):
        if not session.exec(select(Generacion)).first():
            session.add_all(generaciones)
            session.commit()
