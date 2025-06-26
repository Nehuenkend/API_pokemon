from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dependencies.dep_generaciones import init_dep_generaciones
from dependencies.dep_habilidades import init_dep_habilidades
from dependencies.dep_movimientos import init_dep_movimientos
from dependencies.dep_tipos import init_dep_tipos
from dependencies.dep_pokemon import inicializar_dependencia_pokemon
from routes.routes import api_router
from dependencies.sql import get_session, init_engine
from seed.seed import cargar_datos_pokemon


def main():
    init_engine()
    session = next(get_session())

    init_dep_habilidades()
    init_dep_tipos()
    inicializar_dependencia_pokemon()
    init_dep_movimientos()
    init_dep_generaciones()

    cargar_datos_pokemon(session)


app = FastAPI()

origins = ["http://localhost", "http://localhost:5173"]


app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(api_router)

main()
