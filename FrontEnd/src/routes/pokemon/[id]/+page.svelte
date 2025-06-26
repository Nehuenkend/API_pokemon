<script>
  import Footer from "$lib/components/Footer.svelte";
  import Header from "$lib/components/Header.svelte";
  import "$lib/css/tipos.css";

  export let data;
  $: pokemon = data.pokemon;
  let ouptut_estadisticas = {
    ataque: "Ataque",
    defensa: "Defensa",
    ataque_especial: "Ataque Especial",
    defensa_especial: "Defensa Especial",
    puntos_de_golpe: "Puntos de Golpe",
    velocidad: "Velocidad",
  };
</script>

<Header />
<div class="contenedor-pokemon">
  {#if !pokemon}
    <p class="mensaje-no-resultados">No se encontraron resultados.</p>
  {:else}
    <div class="tarjeta-pokemon">
      <div class="contenedor-flex">
        <div class="seccion-principal">
          <div class="info-id-nombre">
            <span class="etiqueta">ID:</span>
            <span class="valor-id">{pokemon.id}</span>
            <h2 class="nombre-pokemon">{pokemon.nombre}</h2>
          </div>
          <div class="imagen-container">
            <img
              class="imagen-pokemon"
              src={pokemon.imagen}
              alt={pokemon.nombre}
            />
          </div>
        </div>
        <div class="seccion-info">
          <div class="seccion-detalles">
            <p>
              <span class="etiqueta">Peso:</span>
              <span class="valor">{pokemon.peso}</span>
            </p>
            <p>
              <span class="etiqueta">Altura:</span>
              <span class="valor">{pokemon.altura}</span>
            </p>
            <p>
              <span class="etiqueta">Generaciones:</span>
              <span class="valor">
                {#if pokemon.generaciones.length > 1}
                  {pokemon.generaciones[[0]].nombre} - {pokemon.generaciones[
                    [pokemon.generaciones.length - 1]
                  ].nombre}
                {:else}
                  {pokemon.generaciones[[pokemon.generaciones.length - 1]]
                    .nombre}
                {/if}</span
              >
            </p>

            <div class="detalles-item">
              <span class="etiqueta">Tipos:</span>
              <div class="tipos-container">
                {#each pokemon.tipos as tipo}
                  <span class="icono-tipo tipo-{tipo.nombre.toLowerCase()}">
                    {tipo.nombre}
                  </span>
                {/each}
              </div>
            </div>

            <div class="detalles-item">
              <span class="etiqueta">Habilidades:</span>
              <div class="valores-lista">
                {#each pokemon.habilidades as habilidad}
                  <span class="valor">{habilidad.nombre || habilidad}</span>
                {/each}
              </div>
            </div>

            <div class="detalles-item">
              <span class="etiqueta">Estadísticas:</span>
              <div class="valores-lista">
                {#each Object.entries(pokemon.estadisticas) as [stat, valor]}
                  <p class="stat-item">
                    <span class="stat-name">{ouptut_estadisticas[stat]}: </span>
                    <span class="stat-value">{valor}</span>
                  </p>{/each}
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>

    <div class="tarjeta-pokemon seccion-ev-mov">
      <div class="detalles-item">
        <span class="etiqueta">Evoluciones:</span>
        <div class="valores-lista">
          {#if pokemon.evoluciones && pokemon.evoluciones.length > 0}
            <ul>
              {#each pokemon.evoluciones as evolucion}
                <div class="evolucion-item">
                  <a href="/pokemon/{evolucion.id}">
                    <img
                      src={evolucion.imagen}
                      alt={evolucion.nombre}
                      class="evolucion-img"
                    /></a
                  >
                  <span>{evolucion.nombre}</span>
                </div>
              {/each}
            </ul>
          {:else}
            <span>No tiene evoluciones.</span>
          {/if}
        </div>
      </div>

      <div class="detalles-item">
        <span class="etiqueta">Movimientos Máquina:</span>
        <div class="valores-lista">
          {#if pokemon.movimientos_maquina && pokemon.movimientos_maquina.length > 0}
            {#each pokemon.movimientos_maquina as mov}
              <span>{mov.nombre} </span>
            {/each}
          {:else}
            <span>No aprende movimientos por máquina.</span>
          {/if}
        </div>
      </div>

      <div class="detalles-item">
        <span class="etiqueta">Movimientos Huevo:</span>
        <div class="valores-lista">
          {#if pokemon.movimientos_huevo && pokemon.movimientos_huevo.length > 0}
            {#each pokemon.movimientos_huevo as mov}
              <span>{mov.nombre} </span>
            {/each}
          {:else}
            <span>No aprende movimientos por huevo.</span>
          {/if}
        </div>
      </div>

      <div class="detalles-item">
        <span class="etiqueta">Movimientos Nivel:</span>
        <div class="valores-lista">
          {#if pokemon.movimientos_nivel && pokemon.movimientos_nivel.length > 0}
            {#each pokemon.movimientos_nivel as mov}
              <span>{mov.nombre} </span>
            {/each}
          {:else}
            <span>No aprende movimientos por nivel.</span>
          {/if}
        </div>
      </div>
    </div>
  {/if}
</div>

<Footer />

<style>
  .contenedor-pokemon {
    padding: 20px;
    max-width: auto;
    margin: 0 50px;
  }
  .tarjeta-pokemon {
    background-color: #ffffff;
    border-radius: 12px;
    box-shadow: 0 4px 15px rgba(0, 0, 0, 0.1);
    padding: 20px;
    display: flex;
    flex-direction: column;
    overflow: hidden;
  }
  .tarjeta-pokemon.zero {
    background-color: #f7f9fc;
  }
  .tarjeta-pokemon.one {
    background-color: #ffffff;
  }
  .contenedor-flex {
    display: flex;
    gap: 32px;
    align-items: flex-start;
  }
  .seccion-principal {
    display: flex;
    flex-direction: column;
    align-items: center;
    margin-bottom: 20px;
    border-bottom: 1px solid #eee;
    padding-bottom: 15px;
    flex: 1;
  }
  .seccion-info {
    display: flex;
    flex-direction: column;
    align-items: center;
    margin-bottom: 20px;
    border-bottom: 1px solid #eee;
    padding-bottom: 15px;
    flex: 2;
  }
  .seccion-ev-mov {
    margin-top: 24px;
  }
  .info-id-nombre {
    text-align: center;
    margin-bottom: 15px;
  }
  .etiqueta {
    font-weight: bold;
    color: #555;
    margin-right: 5px;
  }
  .valor {
    color: #333;
  }
  .valor-id {
    font-size: 1.1em;
    color: #777;
  }
  .nombre-pokemon {
    font-size: 2em;
    font-weight: 700;
    color: #333;
    margin: 5px 0 0 0;
  }
  .imagen-container {
    width: 150px;
    height: 150px;
    display: flex;
    justify-content: center;
    align-items: center;
    background-color: #e0f7fa;
    border-radius: 50%;
    overflow: hidden;
  }
  .imagen-pokemon {
    max-width: 100%;
    max-height: 100%;
    object-fit: contain;
  }
  .seccion-detalles {
    display: flex;
    flex-direction: column;
    gap: 12px;
  }
  .seccion-detalles p {
    margin: 0;
    line-height: 1.5;
  }
  .detalles-item {
    display: flex;
    flex-wrap: wrap;
    gap: 5px;
    align-items: baseline;
  }
  .tipos-container,
  .valores-lista {
    display: flex;
    flex-wrap: wrap;
    gap: 8px;
    margin-top: 5px;
  }
  .icono-tipo {
    display: inline-block;
    padding: 4px 10px;
    border-radius: 20px;
    font-size: 0.85em;
    font-weight: bold;
    color: white;
    text-shadow: 1px 1px 2px rgba(0, 0, 0, 0.2);
  }
  .tipo-normal {
    background-color: #a8a77a;
  }
  .tipo-fuego {
    background-color: #ee812f;
  }
  .tipo-agua {
    background-color: #6390f0;
  }
  .mensaje-no-resultados {
    text-align: center;
    font-size: 1.2em;
    color: #666;
    margin-top: 50px;
    width: 100%;
  }
  .evoluciones-lista {
    display: flex;
    gap: 16px;
    align-items: center;
    margin-top: 8px;
  }
  .evolucion-item {
    display: flex;
    flex-direction: column;
    align-items: center;
  }
  .evolucion-img {
    width: 48px;
    height: 48px;
    object-fit: contain;
    margin-bottom: 4px;
  }
</style>
