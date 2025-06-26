from sqlmodel import JSON, Column, Field, SQLModel
from models.generacion import GeneracionBase
from models.habilidad import HabilidadBase
from models.movimiento import MovimientoBase
from models.pokemon import Pokemon_base
from models.tipo import Tipo_base


class GeneracionPublic(GeneracionBase):
    id: int


class PokemonPublicMov(Pokemon_base):
    id: int


class MovimientoPublicWithRelations(MovimientoBase):
    id: int
    generacion: GeneracionPublic
    pokemon_por_huevo: list[PokemonPublicMov]
    pokemon_por_nivel: list[PokemonPublicMov]
    pokemon_por_maquina: list[PokemonPublicMov]


class MovimientosPublicWithRelations(MovimientoBase):
    id: int
    generacion: GeneracionPublic


class TipoPublic(Tipo_base):
    id: int


class HabilidadPublic(HabilidadBase):
    id: int


class PokemonPublicWithRelations(Pokemon_base):
    id: int
    tipos: list[TipoPublic]
    habilidades: list[HabilidadPublic]
    generaciones: list[GeneracionPublic]
    estadisticas: dict = Field(sa_column=Column(JSON))
    evoluciones: list[dict] | None = Field(sa_column=Column(JSON))
    movimientos_huevo: list[MovimientosPublicWithRelations] | None
    movimientos_maquina: list[MovimientosPublicWithRelations] | None
    movimientos_nivel: list[MovimientosPublicWithRelations] | None


class PokemonPublicParaIntegrante(SQLModel):
    id: int
    nombre: str
    imagen: str
    generaciones: list[GeneracionPublic]
    tipos: list[TipoPublic]


class PokemonesPublicWithRelations(Pokemon_base):
    id: int
    generaciones: list[GeneracionPublic]
    tipos: list[TipoPublic]
