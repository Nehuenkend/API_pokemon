from fastapi import FastAPI
from sqlmodel import Relationship, SQLModel, Field
from typing import List

from models.tablas_intermedias import PokemonGeneracion

app = FastAPI()


class GeneracionBase(SQLModel):
    nombre: str


class Generacion(GeneracionBase, table=True):
    id: int = Field(primary_key=True)
    pokemones: List["Pokemon"] = Relationship(
        back_populates="generaciones", link_model=PokemonGeneracion
    )
    movimientos: List["Movimiento"] = Relationship(back_populates="generacion")
