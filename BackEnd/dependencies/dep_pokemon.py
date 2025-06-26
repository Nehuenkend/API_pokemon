from database.db_pokemon import BaseDatosPokemon
from typing import Annotated
from fastapi import Depends

instancia_base_datos = None


def inicializar_dependencia_pokemon():
    global instancia_base_datos
    instancia_base_datos = BaseDatosPokemon()


def obtener_base_datos() -> BaseDatosPokemon:
    global instancia_base_datos
    if instancia_base_datos is None:
        raise RuntimeError("La base de datos no está inicializada.")
    return instancia_base_datos


DependenciaBaseDatosPokemon = Annotated[BaseDatosPokemon, Depends(obtener_base_datos)]
