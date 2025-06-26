from fastapi import APIRouter
from routes import generaciones
from routes import pokemones
from routes import movimientos
from routes import habilidades
from routes import tipos

api_router = APIRouter(prefix="/API-kachu")

api_router.include_router(
    generaciones.router, prefix="/generaciones", tags=["generacion"]
)
api_router.include_router(pokemones.router, prefix="/pokemones", tags=["pokemones"])
api_router.include_router(
    movimientos.router, prefix="/movimientos", tags=["movimientos"]
)
api_router.include_router(
    habilidades.router, prefix="/habilidades", tags=["habilidades"]
)
api_router.include_router(tipos.router, prefix="/tipos", tags=["tipos"])
