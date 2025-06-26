from typing import List, Optional
from fastapi import Query
from sqlmodel import JSON, Column, Relationship, SQLModel, Field

from models.generacion import Generacion
from .pokemon import Pokemon
from typing import List
from models.tablas_intermedias import (
    PokemonMovimientoNivel,
    PokemonMovimientoHuevo,
    PokemonMovimientoMaquina,
)


class MovimientoBase(SQLModel):
    nombre: str
    tipo: dict | None = Field(sa_column=Column(JSON))
    categoria: str
    potencia: int | None = None
    precision: int | None = None
    pp: int | None = None
    efecto: str


class Movimiento_reducido(MovimientoBase):
    id: int = Field(primary_key=True)
    id_generacion: int = Field(default=None, foreign_key="generacion.id")


class Movimiento(Movimiento_reducido, table=True):
    generacion: Optional["Generacion"] = Relationship(back_populates="movimientos")
    pokemon_por_huevo: List["Pokemon"] | None = Relationship(
        back_populates="movimientos_huevo", link_model=PokemonMovimientoHuevo
    )
    pokemon_por_nivel: List["Pokemon"] | None = Relationship(
        back_populates="movimientos_nivel", link_model=PokemonMovimientoNivel
    )
    pokemon_por_maquina: List["Pokemon"] | None = Relationship(
        back_populates="movimientos_maquina", link_model=PokemonMovimientoMaquina
    )


class FiltrosMovimiento(SQLModel):
    nombre: Optional[str] = Query(default=None)
    tipo: Optional[int] = Query(default=None)
    limit: int = Query(default=10, ge=1)
    offset: int = Query(default=0, ge=0)
