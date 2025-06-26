<script>
  import { goto } from "$app/navigation";
  import { page } from "$app/stores";
  import Footer from "$lib/components/Footer.svelte";
  import Header from "$lib/components/Header.svelte";
  import Pagination from "$lib/components/Pagination.svelte";
  import { onMount } from "svelte";

  let { data } = $props();

  let filtroNombre = $state(data.filtros.nombre || "");
  let filtroTipo = $state(data.filtros.tipo || "");

  let tipos = $state([]);

  onMount(async () => {
    cargarTipos();
  });

  async function cargarTipos() {
    let url = `http://localhost:8000/API-kachu/tipos`;
    const response = await fetch(url, {
      headers: {
        Authorization: "Bearer token",
      },
    });
    if (!response.ok) {
      throw new Error(`Response status: ${response.status}`);
    }
    tipos = await response.json();
  }

  function onSubmit(e) {
    e.preventDefault();
    const url = new URL($page.url);
    url.searchParams.set("page", "0");
    url.searchParams.set("nombre", filtroNombre);
    url.searchParams.set("tipo", filtroTipo);

    goto(url.toString());
  }

  function goToPage(newPage) {
    const url = new URL($page.url);
    url.searchParams.set("page", newPage.toString());
    url.searchParams.set("nombre", filtroNombre);
    url.searchParams.set("tipo", filtroTipo);

    goto(url.toString());
  }

  function nextPage() {
    goToPage(data.currentPage + 1);
  }

  function prevPage() {
    if (data.currentPage > 0) {
      goToPage(data.currentPage - 1);
    }
  }

  function nombres(generaciones) {
    return generaciones.map((g) => g.nombre).join(", ");
  }
</script>

<Header />

<div class="main-content">
  <div class="grilla"></div>
  <div class="columna-filtros-grilla">
    <form class="tabla-filtros" onsubmit={onSubmit}>
      <label for="filtro-nombre">Nombre:</label>
      <input id="filtro-nombre" bind:value={filtroNombre} />

      <label for="filtro-tipo">Tipo:</label>
      <select id="filtro-tipo" bind:value={filtroTipo}>
        <option value="">Todos</option>
        {#each tipos as tipo}
          <option value={tipo.id}>{tipo.nombre}</option>
        {/each}
      </select>
      <button type="submit">Buscar</button>
    </form>

    <div class="grilla">
      <div class="grilla-c">
        <table>
          <thead>
            <tr>
              <th class="columna-superior">Id</th>
              <th class="columna-superior">Nombre</th>
              <th class="columna-superior">Imagen</th>
              <th class="columna-superior">Generaciones</th>
              <th class="columna-superior">Tipos</th>
            </tr>
          </thead>
          <tbody>
            {#if data.pokemones.length === 0}
              <tr>
                <td colspan="5" style="text-align:center;"
                  >No se encontraron resultados.</td
                >
              </tr>
            {:else}
              {#each data.pokemones as pokemon}
                <tr class={pokemon.id % 2 == 0 ? "zero" : "one"}>
                  <td>{pokemon.id}</td>
                  <td><a href="/pokemon/{pokemon.id}">{pokemon.nombre}</a></td>
                  <td>
                    <a href="/pokemon/{pokemon.id}">
                      <img
                        class="imagen-pokemon"
                        src={pokemon.imagen}
                        alt={pokemon.nombre}
                      />
                    </a>
                  </td>
                  <td>
                    {#if pokemon.generaciones.length > 1}
                      {pokemon.generaciones[[0]].nombre} - {pokemon
                        .generaciones[[pokemon.generaciones.length - 1]].nombre}
                    {:else}
                      {pokemon.generaciones[[pokemon.generaciones.length - 1]]
                        .nombre}
                    {/if}
                  </td>
                  <td>
                    {#each pokemon.tipos as tipo}
                      <span class="icono-tipo tipo-{tipo.nombre.toLowerCase()}">
                        {tipo.nombre}
                      </span>
                    {/each}
                  </td>
                </tr>
              {/each}
            {/if}
          </tbody>
        </table>
        <div class="paginado-centro">
          <Pagination
            currentPage={data.currentPage}
            pageSize={data.pageSize}
            hasMore={data.hasMore}
            onPrev={prevPage}
            onNext={nextPage}
          />
        </div>
      </div>
    </div>
  </div>

  <a
    href="/pokemon/creacion"
    class="boton-creacion-flotante"
    aria-label="Crear Pokémon"
  >
    <span class="my-button">Creacion de Pokemon</span>
  </a>
</div>

<Footer />

<style>
  @import "$lib/css/tipos.css";
  @import "$lib/css/styles.css";

  .imagen-pokemon {
    width: 50px;
    height: 50px;
    object-fit: contain;
  }

  .columna-superior {
    background-color: #ecdfec;
  }

  thead {
    display: table-header-group;
    vertical-align: middle;
    unicode-bidi: isolate;
    border-color: inherit;
  }

  tr {
    display: table-row;
    vertical-align: inherit;
    unicode-bidi: isolate;
    border-color: inherit;
  }

  .grilla {
    display: flex;
    flex-wrap: wrap;
    justify-content: center;
    margin: 0;
  }

  .grilla-columna {
    margin-bottom: 1rem;
    padding: 0 1rem;
    width: auto;
  }

  .tabla-filtros {
    margin: 1rem auto 1rem;
    text-align: center;
  }

  .main-content {
    display: flex;
    flex-direction: row;
    margin: 0 auto;
    max-width: 1200px;
    padding: 0 1rem;
    position: relative;
    min-height: calc(100vh - var(--header-height) - var(--footer-height));
    align-items: flex-start;
  }

  .columna-filtros-grilla {
    flex: 1;
    margin-right: 1rem;
  }

  .boton-creacion-flotante {
    position: absolute;
    top: 50%;
    transform: translateY(-50%);
    right: 0;
    margin-right: 1rem;

    display: inline-flex;
    align-items: center;
    justify-content: center;
    width: 48px;
    height: 48px;
    background: linear-gradient(135deg, #ff5959 0%, #f7d02c 100%);
    color: #fff;
    font-size: 2rem;
    font-weight: bold;
    border: none;
    border-radius: 12px;
    text-decoration: none;
    box-shadow: 0 1px 4px rgba(0, 0, 0, 0.1);
    transition:
      background 0.2s,
      color 0.2s,
      transform 0.1s;
    cursor: pointer;
  }

  .boton-creacion-flotante:hover {
    background: linear-gradient(135deg, #f7d02c 0%, #ff5959 100%);
    color: #222;
    transform: translateY(-50%) scale(1.08);
  }

  .my-button {
    padding: 10px 20px;
    background-color: #f3eb11;
    color: white;
    border: none;
    border-radius: 5px;
    cursor: pointer;
  }
  .my-button:hover {
    background-color: #ef9916;
  }
  .my-button:active {
    background-color: #ac0f0f;
  }

  .paginado-centro {
    display: flex;
    justify-content: center;
    margin: 1.5rem 0 0 0;
  }
</style>
