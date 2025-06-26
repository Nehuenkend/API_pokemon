from sqlmodel import Relationship, SQLModel, Field


class PokemonTipo(SQLModel, table=True):
    pokemon_id: int | None = Field(
        default=None, foreign_key="pokemon.id", primary_key=True
    )
    tipo_id: int | None = Field(default=None, foreign_key="tipo.id", primary_key=True)


class PokemonHabilidad(SQLModel, table=True):
    pokemon_id: int | None = Field(
        default=None, foreign_key="pokemon.id", primary_key=True
    )
    habilidad_id: int | None = Field(
        default=None, foreign_key="habilidad.id", primary_key=True
    )


class PokemonMovimientoHuevo(SQLModel, table=True):
    pokemon_id: int | None = Field(
        default=None, foreign_key="pokemon.id", primary_key=True
    )
    movimiento_id: int | None = Field(
        default=None, foreign_key="movimiento.id", primary_key=True
    )


class PokemonMovimientoNivel(SQLModel, table=True):
    pokemon_id: int | None = Field(
        default=None, foreign_key="pokemon.id", primary_key=True
    )
    movimiento_id: int | None = Field(
        default=None, foreign_key="movimiento.id", primary_key=True
    )


class PokemonMovimientoMaquina(SQLModel, table=True):
    pokemon_id: int | None = Field(
        default=None, foreign_key="pokemon.id", primary_key=True
    )
    movimiento_id: int | None = Field(
        default=None, foreign_key="movimiento.id", primary_key=True
    )


class PokemonGeneracion(SQLModel, table=True):
    pokemon_id: int | None = Field(
        default=None, foreign_key="pokemon.id", primary_key=True
    )
    generacion_id: int | None = Field(
        default=None, foreign_key="generacion.id", primary_key=True
    )
