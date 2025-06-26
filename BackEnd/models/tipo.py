from typing import List, Optional
from fastapi import Query
from sqlmodel import Column, Relationship, SQLModel, Field, JSON
from models.tablas_intermedias import PokemonTipo


class Tipo_base(SQLModel):
    nombre: str
    debilidades: list[dict] = Field(sa_column=Column(JSON))


class Tipo(Tipo_base, table=True):
    id: int = Field(primary_key=True)
    pokemones: List["Pokemon"] = Relationship(
        back_populates="tipos", link_model=PokemonTipo
    )


class FiltrosTipo(SQLModel):
    nombre: Optional[str] = Query(default=None)
    limit: int = Query(default=10, ge=1)
    offset: int = Query(default=0, ge=0)
