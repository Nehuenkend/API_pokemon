from sqlmodel import Relationship, SQLModel, Field, Column, JSON
from typing import List, Dict, Optional
from fastapi import Query

from models.tipo import Tipo
from models.tablas_intermedias import (
    PokemonGeneracion,
    PokemonMovimientoHuevo,
    PokemonMovimientoMaquina,
    PokemonMovimientoNivel,
    PokemonTipo,
    PokemonHabilidad,
)
from models.habilidad import Habilidad


class Pokemon_base(SQLModel):
    nombre: str
    imagen: str
    altura: float
    peso: float


class Pokemon(Pokemon_base, table=True):
    id: int = Field(primary_key=True)
    tipos: List[Tipo] = Relationship(back_populates="pokemones", link_model=PokemonTipo)
    habilidades: List[Habilidad] | None = Relationship(
        back_populates="pokemones", link_model=PokemonHabilidad
    )
    estadisticas: dict = Field(sa_column=Column(JSON))
    evoluciones: List[Dict] | None = Field(sa_column=Column(JSON))
    movimientos_huevo: List["Movimiento"] | None = Relationship(
        back_populates="pokemon_por_huevo", link_model=PokemonMovimientoHuevo
    )
    movimientos_maquina: List["Movimiento"] | None = Relationship(
        back_populates="pokemon_por_maquina", link_model=PokemonMovimientoMaquina
    )
    movimientos_nivel: List["Movimiento"] | None = Relationship(
        back_populates="pokemon_por_nivel", link_model=PokemonMovimientoNivel
    )
    generaciones: List["Generacion"] | None = Relationship(
        back_populates="pokemones", link_model=PokemonGeneracion
    )


class PokemonNuevo(SQLModel):
    altura: float
    peso: float
    generaciones: List[int]
    tipos: List[int]
    habilidades: List[int]
    estadisticas: dict
    movimientos_huevo: List[int]
    movimientos_maquina: List[int]
    movimientos_nivel: List[int]
    primer_padre: List[int]
    segundo_padre: List[int]


class FiltrosPokemon(SQLModel):
    nombre: Optional[str] = Query(default=None)
    tipo: Optional[int] = Query(default=None)
    habilidad: Optional[int] = Query(default=None)
    limit: int = Query(default=10, ge=1)
    offset: int = Query(default=0, ge=0)
