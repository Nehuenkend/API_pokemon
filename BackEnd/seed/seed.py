import csv
from sqlmodel import Session, select
from models.movimiento import Movimiento
from dependencies.dep_tipos import get_database as get_tipos_database
from dependencies.dep_habilidades import (
    get_database as get_habilidades_database,
)
from dependencies.dep_movimientos import get_database as get_movimientos_database
from dependencies.dep_generaciones import get_database as get_generaciones_database
from dependencies.dep_movimientos import get_database as get_movimientos_database

from models.habilidad import Habilidad
from models.pokemon import Pokemon
from models.tablas_intermedias import (
    PokemonGeneracion,
    PokemonHabilidad,
    PokemonMovimientoHuevo,
    PokemonMovimientoMaquina,
    PokemonMovimientoNivel,
    PokemonTipo,
)
from models.tipo import Tipo
from models.generacion import Generacion

ruta_repositorio = "../BackEnd"


def cargar_datos_pokemon(session: Session):
    if session.exec(select(Pokemon)).first():
        return

    ruta_pokemon = f"{ruta_repositorio}/data/pokemon.csv"
    generaciones, lista_generaciones = cargar_generaciones(
        f"{ruta_repositorio}/data/pokemon_generations.csv",
        f"{ruta_repositorio}/data/generation_names.csv",
    )
    tipos, tipos_por_id = cargar_tipos(
        f"{ruta_repositorio}/data/pokemon_types.csv",
        f"{ruta_repositorio}/data/type_names.csv",
        f"{ruta_repositorio}/data/type_efficacy.csv",
    )
    habilidades, nombres_habilidades = cargar_habilidades(
        f"{ruta_repositorio}/data/pokemon_abilities.csv",
        f"{ruta_repositorio}/data/ability_names.csv",
    )
    estadisticas = cargar_estadisticas(
        f"{ruta_repositorio}/data/pokemon_stats.csv",
        f"{ruta_repositorio}/data/stat_names.csv",
    )
    evoluciones = cargar_evoluciones(
        f"{ruta_repositorio}/data/pokemon_evolutions.csv",
        f"{ruta_repositorio}/data/pokemon.csv",
    )
    (
        movimientos,
        nombres_movimientos,
        nombres_efectos,
        nombres_damage_class,
        nombres_tipos,
    ) = cargar_movimientos(
        f"{ruta_repositorio}/data/pokemon_moves.csv",
        f"{ruta_repositorio}/data/move_names.csv",
        f"{ruta_repositorio}/data/moves.csv",
        f"{ruta_repositorio}/data/type_names.csv",
        f"{ruta_repositorio}/data/generation_names.csv",
        f"{ruta_repositorio}/data/move_effect_prose.csv",
        f"{ruta_repositorio}/data/pokemon_move_methods.csv",
        ruta_damage_class=f"{ruta_repositorio}/data/move_damage_class_prose.csv",
    )

    lista_habilidades = []

    for habilidad_id, habilidad_nombre in nombres_habilidades.items():
        lista_habilidades.append(Habilidad(id=habilidad_id, nombre=habilidad_nombre))

    lista_tipos = []

    for tipo in tipos_por_id.values():
        lista_tipos.append(Tipo(id=tipo[0], nombre=tipo[1], debilidades=tipo[2]))

    get_habilidades_database().cargar_habilidades(lista_habilidades, session)
    get_tipos_database().cargar_tipos(lista_tipos, session)
    get_generaciones_database().cargar_generaciones(lista_generaciones, session)

    movimientos_definitivo = []
    movimientos_agregados = set()
    for movimientos_pokemon in movimientos.values():
        for metodo in ["huevo", "maquina", "nivel"]:
            for mov in movimientos_pokemon.get(metodo, []):
                mov_id = mov["id"]
                if mov_id in movimientos_agregados:
                    continue
                generacion_mov_actual = session.get(Generacion, mov["generacion"]["id"])
                movimiento = Movimiento(
                    id=mov_id,
                    nombre=mov["nombre"],
                    generacion=generacion_mov_actual,
                    tipo=mov["tipo"],
                    categoria=mov["categoria"],
                    potencia=mov["potencia"],
                    precision=mov["precision"],
                    pp=mov["puntos_de_poder"],
                    efecto=mov["efecto"],
                )
                movimientos_definitivo.append(movimiento)
                movimientos_agregados.add(mov_id)

    get_movimientos_database().cargar_movimientos(movimientos_definitivo, session)

    with open(ruta_pokemon, encoding="utf-8") as archivo:
        lector = csv.DictReader(archivo)
        for fila in lector:
            try:
                id_pokemon = int(fila["id"])

                pokemon = Pokemon(
                    id=id_pokemon,
                    nombre=fila["identifier"],
                    imagen=f"https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/{id_pokemon}.png",
                    altura=float(fila["height"]) / 10,
                    peso=float(fila["weight"]) / 10,
                    estadisticas=estadisticas.get(id_pokemon, {}),
                    evoluciones=evoluciones.get(id_pokemon, []),
                )
                session.add(pokemon)
                session.commit()

                ids_generaciones = [g["id"] for g in generaciones.get(id_pokemon, [])]
                for id_gen in ids_generaciones:
                    session.add(
                        PokemonGeneracion(pokemon_id=id_pokemon, generacion_id=id_gen)
                    )

                ids_habilidades = [h["id"] for h in habilidades.get(id_pokemon, [])]

                for id_hab in ids_habilidades:
                    session.add(
                        PokemonHabilidad(pokemon_id=id_pokemon, habilidad_id=id_hab)
                    )
                ids_tipos = [t["id"] for t in tipos.get(id_pokemon, [])]
                for id_tipo in ids_tipos:
                    session.add(PokemonTipo(pokemon_id=id_pokemon, tipo_id=id_tipo))
                movimientos_actual = movimientos.get(id_pokemon, {})
                ids_mov_h = [m["id"] for m in movimientos_actual.get("huevo", [])]
                for id_mov_h in ids_mov_h:
                    session.add(
                        PokemonMovimientoHuevo(
                            pokemon_id=id_pokemon, movimiento_id=id_mov_h
                        )
                    )
                ids_mov_m = [m["id"] for m in movimientos_actual.get("maquina", [])]
                for id_mov_m in ids_mov_m:
                    session.add(
                        PokemonMovimientoMaquina(
                            pokemon_id=id_pokemon, movimiento_id=id_mov_m
                        )
                    )
                ids_mov_n = [m["id"] for m in movimientos_actual.get("nivel", [])]
                for id_mov_n in ids_mov_n:
                    session.add(
                        PokemonMovimientoNivel(
                            pokemon_id=id_pokemon, movimiento_id=id_mov_n
                        )
                    )
                session.commit()
            except Exception:
                pass


def cargar_generaciones(ruta_generaciones, ruta_nombres):
    nombres_generaciones = {}
    with open(ruta_nombres, encoding="utf-8") as archivo:
        lector = csv.DictReader(archivo)
        for fila in lector:
            if int(fila["local_language_id"]) == 7:
                nombres_generaciones[int(fila["generation_id"])] = fila["name"]

    generaciones = {}
    lista_generaciones = []
    with open(ruta_generaciones, encoding="utf-8") as archivo:
        lector = csv.DictReader(archivo)
        ids_generaciones_agregadas = set()
        for fila in lector:
            id_pokemon = int(fila["pokemon_id"])
            id_generacion = int(fila["generation_id"])
            if id_pokemon not in generaciones:
                generaciones[id_pokemon] = []
            if id_generacion not in generaciones[id_pokemon]:
                generaciones[id_pokemon].append(
                    {
                        "id": id_generacion,
                        "nombre": nombres_generaciones.get(
                            id_generacion, "Desconocido"
                        ),
                    }
                )
            # Solo agregamos una vez cada generación
            if id_generacion not in ids_generaciones_agregadas:
                lista_generaciones.append(
                    Generacion(
                        id=id_generacion,
                        nombre=nombres_generaciones.get(
                            id_generacion, f"Generación {id_generacion}"
                        ),
                    )
                )
                ids_generaciones_agregadas.add(id_generacion)

    return generaciones, lista_generaciones


def cargar_tipos(ruta_tipos, ruta_nombres, ruta_eficacia):
    """carga tipos y debilidades"""

    tipos_por_id = {}
    nombres_tipos = {}
    with open(ruta_nombres, encoding="utf-8") as archivo:
        lector = csv.DictReader(archivo)
        for fila in lector:
            if int(fila["local_language_id"]) == 7:
                nombres_tipos[int(fila["type_id"])] = fila["name"]
                tipos_por_id[int(fila["type_id"])] = [
                    int(fila["type_id"]),
                    fila["name"],
                ]

    debilidades = {}  # {id: debilidades}
    with open(ruta_eficacia, encoding="utf-8") as archivo:
        lector = csv.DictReader(archivo)
        for fila in lector:
            id_tipo_objetivo = int(fila["target_type_id"])
            id_tipo_dano = int(fila["damage_type_id"])
            factor_dano = int(fila["damage_factor"])
            if factor_dano > 100:
                if id_tipo_objetivo not in debilidades:
                    debilidades[id_tipo_objetivo] = []
                debilidades[id_tipo_objetivo].append(
                    {
                        "id": id_tipo_dano,
                        "nombre": nombres_tipos.get(id_tipo_dano, "Desconocido"),
                    }
                )

    for id_tipo in tipos_por_id:
        tipos_por_id[id_tipo].append(debilidades.get(id_tipo))

    tipos = {}  # {id_pokemon: [{id,nombre, debilidades}]}
    with open(ruta_tipos, encoding="utf-8") as archivo:
        lector = csv.DictReader(archivo)
        for fila in lector:
            id_pokemon = int(fila["pokemon_id"])
            id_tipo = int(fila["type_id"])
            if id_pokemon not in tipos:
                tipos[id_pokemon] = []
            tipos[id_pokemon].append(
                {
                    "id": id_tipo,
                    "nombre": nombres_tipos.get(id_tipo, "Desconocido"),
                    "debilidades": debilidades.get(id_tipo, []),
                }
            )

    tipos_output = {}
    for tipo in tipos_output:
        for tipo_id, nombre in tipo.values():
            tipos_output[tipo_id] = {
                "id": tipo_id,
                "nombre": nombre,
                "debilidades": debilidades.get(tipo_id, []),
            }

    return tipos, tipos_por_id


def cargar_habilidades(ruta_habilidades, ruta_nombres):
    nombres_habilidades = {}
    with open(ruta_nombres, encoding="utf-8") as archivo:
        lector = csv.DictReader(archivo)
        for fila in lector:
            if int(fila["local_language_id"]) == 7:
                nombres_habilidades[int(fila["ability_id"])] = fila["name"]

    habilidades = {}  # {<pokemon_id>: [{"id_habilidad", "nombre"}]}
    with open(ruta_habilidades, encoding="utf-8") as archivo:
        lector = csv.DictReader(archivo)
        for fila in lector:
            id_pokemon = int(fila["pokemon_id"])
            id_habilidad = int(fila["ability_id"])
            if id_pokemon not in habilidades:
                habilidades[id_pokemon] = []
            habilidades[id_pokemon].append(
                {
                    "id": id_habilidad,
                    "nombre": nombres_habilidades.get(id_habilidad, "Desconocido"),
                }
            )
    return habilidades, nombres_habilidades


def cargar_estadisticas(ruta_estadisticas, ruta_nombres):

    nombres_estadisticas = {
        int(fila["stat_id"]): fila["name"].lower()
        for fila in csv.DictReader(open(ruta_nombres, encoding="utf-8"))
        if int(fila["local_language_id"]) == 7
    }

    mapeo_estadisticas = {
        "ataque": "ataque",
        "defensa": "defensa",
        "ataque especial": "ataque_especial",
        "defensa especial": "defensa_especial",
        "ps": "puntos_de_golpe",
        "velocidad": "velocidad",
    }

    estadisticas = {}
    with open(ruta_estadisticas, encoding="utf-8") as archivo:
        for fila in csv.DictReader(archivo):
            id_pokemon = int(fila["pokemon_id"])
            id_estadistica = int(fila["stat_id"])
            valor_base = int(fila["base_stat"])
            estadisticas.setdefault(
                id_pokemon, {key: 0 for key in mapeo_estadisticas.values()}
            )
            nombre_estadistica = nombres_estadisticas.get(id_estadistica, "").lower()
            clave_estadistica = mapeo_estadisticas.get(nombre_estadistica)
            if clave_estadistica:
                estadisticas[id_pokemon][clave_estadistica] = valor_base

    return estadisticas


def cargar_evoluciones(ruta_evoluciones, ruta_pokemon):
    """carga las evoluciones asociadas a cada pokemon"""
    nombres_pokemon = {}
    with open(ruta_pokemon, encoding="utf-8") as archivo:
        lector = csv.DictReader(archivo)
        for fila in lector:
            nombres_pokemon[int(fila["id"])] = fila["identifier"]

    evoluciones = {}
    with open(ruta_evoluciones, encoding="utf-8") as archivo:
        lector = csv.DictReader(archivo)
        for fila in lector:
            id_pokemon = int(fila["id"])
            id_evolucion = int(fila["evolution_id"])
            if id_pokemon not in evoluciones:
                evoluciones[id_pokemon] = []
            evoluciones[id_pokemon].append(
                {
                    "id": id_evolucion,
                    "nombre": nombres_pokemon.get(id_evolucion, "Desconocido"),
                    "imagen": f"https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/{id_evolucion}.png",
                }
            )
    return evoluciones


def cargar_movimientos(
    ruta_movimientos,
    ruta_nombres,
    ruta_datos,
    ruta_tipos,
    ruta_generaciones,
    ruta_efectos,
    ruta_metodos,
    ruta_damage_class=None,
):
    nombres_movimientos = {}
    with open(ruta_nombres, encoding="utf-8") as archivo:
        lector = csv.DictReader(archivo)
        for fila in lector:
            if int(fila["local_language_id"]) == 7:
                nombres_movimientos[int(fila["move_id"])] = fila["name"]

    efectos_movimientos = {}
    with open(ruta_efectos, encoding="utf-8") as archivo:
        lector = csv.DictReader(archivo)
        for fila in lector:
            if int(fila["local_language_id"]) == 9:
                efectos_movimientos[int(fila["move_effect_id"])] = fila["short_effect"]

    nombres_damage_class = {}
    if ruta_damage_class:
        with open(ruta_damage_class, encoding="utf-8") as archivo:
            lector = csv.DictReader(archivo)
            for fila in lector:
                if int(fila["local_language_id"]) == 7:
                    nombres_damage_class[int(fila["move_damage_class_id"])] = fila[
                        "name"
                    ]

    nombres_tipos = {}
    with open(ruta_tipos, encoding="utf-8") as archivo:
        lector = csv.DictReader(archivo)
        for fila in lector:
            if int(fila["local_language_id"]) == 7:
                id_tipo = int(fila["type_id"])
                nombres_tipos[id_tipo] = fila["name"]

    # se hace dos veces, optimizar
    nombres_generaciones = {}  # <gen_id> : <name>
    with open(ruta_generaciones, encoding="utf-8") as f:
        csvFile = csv.DictReader(f, delimiter=",")
        for linea in csvFile:
            if linea["local_language_id"] == "7":
                generation_id = int(linea["generation_id"])
                nombres_generaciones[generation_id] = linea["name"]

    movimientos_info = {}
    with open(ruta_datos, encoding="utf-8") as archivo:
        lector = csv.DictReader(archivo)
        for fila in lector:
            id_movimiento = int(fila["id"])
            id_efecto = int(fila["effect_id"])
            movimientos_info[id_movimiento] = {
                "id": id_movimiento,
                "nombre": nombres_movimientos.get(id_movimiento, "Desconocido"),
                "generacion": {
                    "id": int(fila["generation_id"]),
                    "nombre": fila["generation_id"],
                },
                "tipo": {"id": int(fila["type_id"]), "nombre": "Desconocido"},
                "categoria": (
                    "físico"
                    if fila["damage_class_id"] == "2"
                    else "especial" if fila["damage_class_id"] == "3" else "estado"
                ),
                "potencia": int(fila["power"]) if fila["power"] else None,
                "precision": int(fila["accuracy"]) if fila["accuracy"] else None,
                "puntos_de_poder": int(fila["pp"]) if fila["pp"] else None,
                "efecto": efectos_movimientos.get(id_efecto, None),
            }

    with open(ruta_tipos, encoding="utf-8") as archivo:
        lector = csv.DictReader(archivo)
        for fila in lector:
            if int(fila["local_language_id"]) == 7:
                id_tipo = int(fila["type_id"])
                for movimiento in movimientos_info.values():
                    if movimiento["tipo"]["id"] == id_tipo:
                        movimiento["tipo"]["nombre"] = fila["name"]

    metodos_aprendizaje = {}
    with open(ruta_metodos, encoding="utf-8") as archivo:
        lector = csv.DictReader(archivo)
        for fila in lector:
            if int(fila["local_language_id"]) == 7:
                id_metodo = int(fila["pokemon_move_method_id"])
                metodos_aprendizaje[id_metodo] = fila["name"]

    movimientos = {}
    with open(ruta_movimientos, encoding="utf-8") as archivo:
        lector = csv.DictReader(archivo)
        for fila in lector:
            id_pokemon = int(fila["pokemon_id"])
            id_movimiento = int(fila["move_id"])
            id_metodo = int(fila["pokemon_move_method_id"])

            if id_pokemon not in movimientos:
                movimientos[id_pokemon] = {"huevo": [], "maquina": [], "nivel": []}

            movimiento = movimientos_info.get(
                id_movimiento, {"id": id_movimiento, "nombre": "Desconocido"}
            )

            if id_metodo == 1:  # nivel
                if not any(
                    m["id"] == movimiento["id"]
                    for m in movimientos[id_pokemon]["nivel"]
                ):
                    movimientos[id_pokemon]["nivel"].append(movimiento)
            elif id_metodo == 2:  # huevo
                if not any(
                    m["id"] == movimiento["id"]
                    for m in movimientos[id_pokemon]["huevo"]
                ):
                    movimientos[id_pokemon]["huevo"].append(movimiento)
            elif id_metodo == 4:  # maquina
                if not any(
                    m["id"] == movimiento["id"]
                    for m in movimientos[id_pokemon]["maquina"]
                ):
                    movimientos[id_pokemon]["maquina"].append(movimiento)

    return (
        movimientos,
        nombres_movimientos,
        efectos_movimientos,
        nombres_damage_class,
        nombres_tipos,
    )
