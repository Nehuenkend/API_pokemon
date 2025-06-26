<script>
  import { goto } from "$app/navigation";
  import { page } from "$app/stores";
  import Footer from "$lib/components/Footer.svelte";
  import Header from "$lib/components/Header.svelte";
  import Pagination from "$lib/components/Pagination.svelte";

  let { data } = $props();

  let filtroNombre = $state(data.filtros.nombre);
  let movimientos = data.movimientos;

  function onSubmit(e) {
    e.preventDefault();
    const url = new URL($page.url);
    url.searchParams.set("page", "0");
    url.searchParams.set("nombre", filtroNombre);
    goto(url.toString());
  }

  function goToPage(newPage) {
    const url = new URL($page.url);
    url.searchParams.set("page", newPage.toString());
    url.searchParams.set("nombre", filtroNombre);
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
</script>

<Header />

<form class="filtros_movimientos" onsubmit={onSubmit}>
  <label for="filtro-nombre">Nombre:</label>
  <input
    id="filtro-nombre"
    name="nombre"
    bind:value={filtroNombre}
    placeholder="Busca un movimiento"
  />
  <button type="submit">Buscar</button>
</form>

{#if data.movimientos.length > 0}
  <div class="tabla_mov">
    <div class="columnas">
      <table>
        <thead>
          <tr>
            <th>id</th>
            <th>nombre</th>
            <th>generacion</th>
            <th>tipo</th>
            <th>categoria</th>
            <th>potencia</th>
            <th>precision</th>
            <th>pp</th>
            <th>efecto</th>
          </tr>
        </thead>
        <tbody>
          {#each data.movimientos as Movimiento}
            <tr class={Movimiento.id % 2 === 0 ? "zero" : "one"}>
              <td>{Movimiento.id}</td>
              <td>{Movimiento.nombre}</td>
              <td>{Movimiento.generacion.nombre}</td>
              <td>
                {#if Movimiento.tipo}
                  <span
                    class={"icono-tipo tipo-" +
                      Movimiento.tipo.nombre.toLowerCase()}
                  >
                    {Movimiento.tipo.nombre}
                  </span>
                {:else}
                  —
                {/if}
              </td>
              <td>{Movimiento.categoria}</td>
              <td>{Movimiento.potencia ?? "—"}</td>
              <td>{Movimiento.precision ?? "—"}</td>
              <td>{Movimiento.puntos_de_poder ?? "—"}</td>
              <td>{Movimiento.efecto}</td>
            </tr>
          {/each}
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
{:else}
  <p style="margin: 1rem; font-style: italic;">
    No se encontraron movimientos con ese filtro.
  </p>
{/if}
<Footer />

<style>
  @import "$lib/css/styles.css";
  @import "$lib/css/tipos.css";
  .indices {
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
  .tabla_mov {
    display: flex;
    flex-wrap: wrap;
    justify-content: center;
    margin: 0;
  }
  .columnas {
    margin-bottom: 1rem;
    padding: 0 1rem;
    width: auto;
  }
  .filtros_movimientos {
    margin: 1rem auto 1rem;
    text-align: center;
  }
  .paginado-centro {
    display: flex;
    justify-content: center;
    margin: 1.5rem 0 0 0;
  }
</style>
