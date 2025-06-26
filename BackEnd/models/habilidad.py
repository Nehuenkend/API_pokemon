from typing import List, Optional
from fastapi import Query
from sqlmodel import Relationship, SQLModel, Field
from models.tablas_intermedias import PokemonHabilidad


class HabilidadBase(SQLModel):
    nombre: str


class Habilidad(HabilidadBase, table=True):
    id: int = Field(primary_key=True)
    pokemones: List["Pokemon"] = Relationship(
        back_populates="habilidades", link_model=PokemonHabilidad
    )


class FiltrosHabilidad(SQLModel):
    nombre: Optional[str] = Query(default=None)
    limit: int = Query(default=10, ge=1)
    offset: int = Query(default=0, ge=0)
