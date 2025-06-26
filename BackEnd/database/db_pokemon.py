from fastapi import HTTPException
from sqlmodel import Session, select
from models.generacion import Generacion
from models.habilidad import Habilidad
from models.movimiento import Movimiento
from models.pokemon import (
    FiltrosPokemon,
    Pokemon,
    PokemonNuevo,
)
from models.tipo import Tipo


class BaseDatosPokemon:

    def obtener_pokemon(self, session: Session, id_pokemon: int) -> Pokemon:
        pokemon = session.get(Pokemon, id_pokemon)
        if not pokemon:
            return None
        return pokemon

    def listar_pokemones(self, session: Session, filters: FiltrosPokemon):
        query = self._build_list_query(filters)
        pokemones = session.exec(query).all()
        return pokemones

    def _build_list_query(self, filters: FiltrosPokemon):
        query = select(Pokemon)
        if filters:
            filtros_dict = filters.model_dump(
                exclude=["limit", "offset"], exclude_none=True
            )
            for key, val in filtros_dict.items():
                if key == "nombre":
                    query = query.where(Pokemon.nombre.ilike(f"%{val}%"))
                elif key == "tipo":
                    query = query.where(Pokemon.tipos.any(Tipo.id == val))
                elif key == "habilidad":
                    query = query.where(Pokemon.habilidades.any(Habilidad.id == val))
                else:
                    query = query.where(getattr(Pokemon, key) == val)

        query = query.limit(filters.limit).offset(filters.offset)
        return query

    def crear_pokemon(self, session: Session, pokemon_nuevo: PokemonNuevo):
        padre_1 = session.exec(
            select(Pokemon).where(Pokemon.id == pokemon_nuevo.primer_padre[0])
        ).first()
        padre_2 = session.exec(
            select(Pokemon).where(Pokemon.id == pokemon_nuevo.segundo_padre[0])
        ).first()
        habilidades_p_n = session.exec(
            select(Habilidad).where(Habilidad.id.in_(pokemon_nuevo.habilidades))
        ).all()
        generaciones_p_n = session.exec(
            select(Generacion).where(Generacion.id.in_(pokemon_nuevo.generaciones))
        ).all()
        tipos_p_n = session.exec(
            select(Tipo).where(Tipo.id.in_(pokemon_nuevo.tipos))
        ).all()
        movimientos_huevo_p_n = session.exec(
            select(Movimiento).where(Movimiento.id.in_(pokemon_nuevo.movimientos_huevo))
        ).all()
        movimientos_maquina_p_n = session.exec(
            select(Movimiento).where(
                Movimiento.id.in_(pokemon_nuevo.movimientos_maquina)
            )
        ).all()
        movimientos_nivel_p_n = session.exec(
            select(Movimiento).where(Movimiento.id.in_(pokemon_nuevo.movimientos_nivel))
        ).all()
        id_nuevo = len(session.exec(select(Pokemon)).all()) + 1
        print(f"\n\n{id_nuevo}\n\n")

        pokemon = Pokemon(
            id=id_nuevo,
            nombre=f"{padre_1.nombre[:3]}{padre_2.nombre[-3:]}",
            imagen=f"https://images.alexonsager.net/pokemon/fused/{pokemon_nuevo.segundo_padre[0]}/{pokemon_nuevo.segundo_padre[0]}.{pokemon_nuevo.primer_padre[0]}.png",
            altura=pokemon_nuevo.altura,
            peso=pokemon_nuevo.peso,
            habilidades=habilidades_p_n,
            generaciones=generaciones_p_n,
            tipos=tipos_p_n,
            movimientos_nivel=movimientos_nivel_p_n,
            movimientos_huevo=movimientos_huevo_p_n,
            movimientos_maquina=movimientos_maquina_p_n,
            estadisticas=pokemon_nuevo.estadisticas,
        )

        def safe_sum(valores):
            return sum(v for v in valores if v is not None)

        promedio = (
            safe_sum(padre_1.estadisticas.values())
            + safe_sum(padre_2.estadisticas.values())
        ) / 2
        promedio = round(promedio)

        if safe_sum(pokemon.estadisticas.values()) != promedio:
            raise HTTPException(
                status_code=400,
                detail=f"Las estadísticas no coinciden con el promedio de los padres: {promedio}",
            )

        ids_tipos_padres = set(
            [tipo.id for tipo in padre_1.tipos] + [tipo.id for tipo in padre_2.tipos]
        )
        for tipo in pokemon.tipos:
            if tipo.id not in ids_tipos_padres:
                raise HTTPException(
                    status_code=400,
                    detail=f"Tipo {tipo.nombre} no válido para los padres",
                )

        ids_habilidades_padres = set(
            [hab.id for hab in padre_1.habilidades]
            + [hab.id for hab in padre_2.habilidades]
        )

        for hab in pokemon.habilidades:
            if hab.id not in ids_habilidades_padres:
                raise HTTPException(
                    status_code=400,
                    detail=f"Habilidad {hab.nombre} no es válida para los padres",
                )

        ids_mov_nivel_padres = set(
            [mov.id for mov in padre_1.movimientos_nivel]
            + [mov.id for mov in padre_2.movimientos_nivel]
        )
        for mov in pokemon.movimientos_nivel:
            if mov.id not in ids_mov_nivel_padres:
                raise HTTPException(
                    status_code=400,
                    detail=f"Movimiento de nivel {mov.nombre} no es válido para los padres",
                )

        ids_mov_huevo_padres = set(
            [mov.id for mov in padre_1.movimientos_huevo]
            + [mov.id for mov in padre_2.movimientos_huevo]
        )
        for mov in pokemon.movimientos_huevo:
            if mov.id not in ids_mov_huevo_padres:
                raise HTTPException(
                    status_code=400,
                    detail=f"Movimiento de huevo {mov.nombre} no es válido para los padres",
                )

        ids_mov_maquina_padres = set(
            [mov.id for mov in padre_1.movimientos_maquina]
            + [mov.id for mov in padre_2.movimientos_maquina]
        )

        for mov in pokemon.movimientos_maquina:
            if mov.id not in ids_mov_maquina_padres:
                raise HTTPException(
                    status_code=400,
                    detail=f"Movimiento de máquina {mov.nombre} no es válido para los padres",
                )

        if pokemon.altura != float(padre_1.altura) and pokemon.altura != padre_2.altura:
            raise HTTPException(
                status_code=400,
                detail=f"La altura no coincide con ninguna altura de la de los padres ({padre_1.altura} o {padre_2.altura})",
            )

        if pokemon.peso != padre_1.peso and pokemon.peso != padre_2.peso:
            raise HTTPException(
                status_code=400,
                detail=f"El peso no coincide con ningun peso de los padres ({padre_1.peso} o {padre_2.peso})",
            )

        session.add(pokemon)
        session.commit()
        session.refresh(pokemon)
        return pokemon
