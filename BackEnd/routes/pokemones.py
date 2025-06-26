from typing import Annotated
from fastapi import APIRouter, HTTPException, Query
from dependencies.dep_pokemon import DependenciaBaseDatosPokemon
from dependencies.sql import SessionDep
from models.pokemon import FiltrosPokemon, PokemonNuevo
from models.public import PokemonPublicWithRelations, PokemonesPublicWithRelations

router = APIRouter()


@router.get("/{id}")
def obtener_pokemon(
    id: int, session: SessionDep, db: DependenciaBaseDatosPokemon
) -> PokemonPublicWithRelations:
    pokemon = db.obtener_pokemon(session, id)
    if not pokemon:
        raise HTTPException(status_code=404, detail="Pokemon no encontrado")
    return pokemon


@router.get("/")
def listar_pokemones(
    session: SessionDep,
    db: DependenciaBaseDatosPokemon,
    filtros: Annotated[FiltrosPokemon, Query()],
) -> list[PokemonesPublicWithRelations]:
    return db.listar_pokemones(session, filtros)


@router.post("/")
def crear_pokemon(
    session: SessionDep, db: DependenciaBaseDatosPokemon, pokemon: PokemonNuevo
) -> PokemonPublicWithRelations:
    return db.crear_pokemon(session, pokemon)
