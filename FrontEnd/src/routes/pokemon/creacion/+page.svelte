<script>
  import { enhance } from "$app/forms";
  import Footer from "$lib/components/Footer.svelte";
  import Header from "$lib/components/Header.svelte";
  import { onDestroy } from "svelte";

  const { data, form } = $props();

  let generaciones = data.generaciones;

  let pokemon_nuevo = $state({
    altura: "",
    peso: "",
    generaciones: [],
    tipos: [],
    habilidades: [],
    estadisticas: {
      ataque: "",
      defensa: "",
      ataque_especial: "",
      defensa_especial: "",
      puntos_de_golpe: "",
      velocidad: "",
    },
    movimientos_huevo: [],
    movimientos_maquina: [],
    movimientos_nivel: [],
    primer_padre: null,
    segundo_padre: null,
  });

  // Primer padre
  let query1 = $state("");
  let results1 = $state([]);
  let showDropdown1 = $state(false);
  let timeout1;

  function onInput1() {
    clearTimeout(timeout1);
    if (query1.length < 2) {
      results1 = [];
      showDropdown1 = false;
      return;
    }
    timeout1 = setTimeout(fetchResults1, 300);
  }

  function selectResult1(result) {
    query1 = result.nombre;
    showDropdown1 = false;
    pokemon_nuevo.primer_padre = result.id;
  }
  async function fetchResults1() {
    let url = new URL(`http://localhost:8000/API-kachu/pokemones/`);
    let params = { nombre: query1 };
    url.search = new URLSearchParams(params).toString();

    const response = await fetch(url, {
      method: "GET",
      headers: { "Content-Type": "application/json" },
    });
    if (!response.ok) {
      error(response.status, response);
    }

    results1 = await response.json();
    showDropdown1 = results1.length > 0;
  }

  function handleBlur1() {
    setTimeout(() => (showDropdown1 = false), 150);
  }

  // Segundo padre
  let query2 = $state("");
  let results2 = $state([]);
  let showDropdown2 = $state(false);
  let timeout2;

  function onInput2() {
    clearTimeout(timeout2);
    if (query2.length < 2) {
      results2 = [];
      showDropdown2 = false;
      return;
    }
    timeout2 = setTimeout(fetchResults2, 300);
  }

  function selectResult2(result) {
    query2 = result.nombre;
    showDropdown2 = false;
    pokemon_nuevo.segundo_padre = result.id;
  }
  async function fetchResults2() {
    let url = new URL(`http://localhost:8000/API-kachu/pokemones/`);
    let params = { nombre: query2 };
    url.search = new URLSearchParams(params).toString();

    const response = await fetch(url, {
      method: "GET",
      headers: { "Content-Type": "application/json" },
    });
    if (!response.ok) {
      error(response.status, response);
    }

    results2 = await response.json();
    showDropdown2 = results2.length > 0;
  }

  function handleBlur2() {
    setTimeout(() => (showDropdown2 = false), 150);
  }

  // Tipos
  let queryTipo = $state("");
  let resultsTipo = $state([]);
  let showDropdownTipo = $state(false);
  if (!pokemon_nuevo.tipos) pokemon_nuevo.tipos = [];
  let timeoutTipo;
  function onInputTipo() {
    clearTimeout(timeoutTipo);
    if (queryTipo.length < 2) {
      resultsTipo = [];
      showDropdownTipo = false;
      return;
    }
    timeoutTipo = setTimeout(fetchResultsTipo, 300);
  }
  async function fetchResultsTipo() {
    let url = new URL(`http://localhost:8000/API-kachu/tipos/`);
    url.search = new URLSearchParams({ nombre: queryTipo }).toString();
    const response = await fetch(url);
    if (response.ok) {
      resultsTipo = await response.json();
      showDropdownTipo = resultsTipo.length > 0;
    }
  }
  function selectResultTipo(result) {
    if (!pokemon_nuevo.tipos.includes(result.id)) {
      pokemon_nuevo.tipos = [...pokemon_nuevo.tipos, result.id];
    }
    queryTipo = "";
    showDropdownTipo = false;
  }
  function removeTipo(id) {
    pokemon_nuevo.tipos = pokemon_nuevo.tipos.filter((t) => t !== id);
  }
  function handleBlurTipo() {
    setTimeout(() => (showDropdownTipo = false), 150);
  }
  function nombreTipoPorId(id) {
    const found = resultsTipo.find((h) => h.id === id);
    return found ? found.nombre : id;
  }

  // Habilidades
  let queryHabilidad = $state("");
  let resultsHabilidad = $state([]);
  let showDropdownHabilidad = $state(false);
  if (!pokemon_nuevo.habilidades) pokemon_nuevo.habilidades = [];
  let timeoutHabilidad;
  function onInputHabilidad() {
    clearTimeout(timeoutHabilidad);
    if (queryHabilidad.length < 2) {
      resultsHabilidad = [];
      showDropdownHabilidad = false;
      return;
    }
    timeoutHabilidad = setTimeout(fetchResultsHabilidad, 300);
  }
  async function fetchResultsHabilidad() {
    let url = new URL(`http://localhost:8000/API-kachu/habilidades/`);
    url.search = new URLSearchParams({ nombre: queryHabilidad }).toString();
    const response = await fetch(url);
    if (response.ok) {
      resultsHabilidad = await response.json();
      showDropdownHabilidad = resultsHabilidad.length > 0;
    }
  }
  function selectResultHabilidad(result) {
    if (!pokemon_nuevo.habilidades.includes(result.id)) {
      pokemon_nuevo.habilidades = [...pokemon_nuevo.habilidades, result.id];
    }
    queryHabilidad = "";
    showDropdownHabilidad = false;
  }
  function removeHabilidad(id) {
    pokemon_nuevo.habilidades = pokemon_nuevo.habilidades.filter(
      (h) => h !== id
    );
  }
  function handleBlurHabilidad() {
    setTimeout(() => (showDropdownHabilidad = false), 150);
  }
  function nombreHabilidadPorId(id) {
    const found = resultsHabilidad.find((h) => h.id === id);
    return found ? found.nombre : id;
  }

  // Movimientos por huevo
  let queryMovHuevo = $state("");
  let resultsMovHuevo = $state([]);
  let showDropdownMovHuevo = $state(false);
  if (!pokemon_nuevo.movimientos_huevo) pokemon_nuevo.movimientos_huevo = [];
  let timeoutMovHuevo;
  function onInputMovHuevo() {
    clearTimeout(timeoutMovHuevo);
    if (queryMovHuevo.length < 2) {
      resultsMovHuevo = [];
      showDropdownMovHuevo = false;
      return;
    }
    timeoutMovHuevo = setTimeout(fetchResultsMovHuevo, 300);
  }
  async function fetchResultsMovHuevo() {
    let url = new URL(`http://localhost:8000/API-kachu/movimientos/`);
    url.search = new URLSearchParams({ nombre: queryMovHuevo }).toString();
    const response = await fetch(url);
    if (response.ok) {
      resultsMovHuevo = await response.json();
      showDropdownMovHuevo = resultsMovHuevo.length > 0;
    }
  }
  function selectResultMovHuevo(result) {
    if (!pokemon_nuevo.movimientos_huevo.includes(result.id)) {
      pokemon_nuevo.movimientos_huevo = [
        ...pokemon_nuevo.movimientos_huevo,
        result.id,
      ];
    }
    queryMovHuevo = "";
    showDropdownMovHuevo = false;
  }
  function removeMovHuevo(id) {
    pokemon_nuevo.movimientos_huevo = pokemon_nuevo.movimientos_huevo.filter(
      (m) => m !== id
    );
  }
  function handleBlurMovHuevo() {
    setTimeout(() => (showDropdownMovHuevo = false), 150);
  }
  function nombreMovHuevoPorId(id) {
    const found = resultsMovHuevo.find((m) => m.id === id);
    return found ? found.nombre : id;
  }

  // Movimientos por máquina
  let queryMovMaquina = $state("");
  let resultsMovMaquina = $state([]);
  let showDropdownMovMaquina = $state(false);
  if (!pokemon_nuevo.movimientos_maquina)
    pokemon_nuevo.movimientos_maquina = [];
  let timeoutMovMaquina;
  function onInputMovMaquina() {
    clearTimeout(timeoutMovMaquina);
    if (queryMovMaquina.length < 2) {
      resultsMovMaquina = [];
      showDropdownMovMaquina = false;
      return;
    }
    timeoutMovMaquina = setTimeout(fetchResultsMovMaquina, 300);
  }
  async function fetchResultsMovMaquina() {
    let url = new URL(`http://localhost:8000/API-kachu/movimientos/`);
    url.search = new URLSearchParams({ nombre: queryMovMaquina }).toString();
    const response = await fetch(url);
    if (response.ok) {
      resultsMovMaquina = await response.json();
      showDropdownMovMaquina = resultsMovMaquina.length > 0;
    }
  }
  function selectResultMovMaquina(result) {
    if (!pokemon_nuevo.movimientos_maquina.includes(result.id)) {
      pokemon_nuevo.movimientos_maquina = [
        ...pokemon_nuevo.movimientos_maquina,
        result.id,
      ];
    }
    queryMovMaquina = "";
    showDropdownMovMaquina = false;
  }
  function removeMovMaquina(id) {
    pokemon_nuevo.movimientos_maquina =
      pokemon_nuevo.movimientos_maquina.filter((m) => m !== id);
  }
  function handleBlurMovMaquina() {
    setTimeout(() => (showDropdownMovMaquina = false), 150);
  }
  function nombreMovMaquinaPorId(id) {
    const found = resultsMovMaquina.find((m) => m.id === id);
    return found ? found.nombre : id;
  }

  // Movimientos por nivel
  let queryMovNivel = $state("");
  let resultsMovNivel = $state([]);
  let showDropdownMovNivel = $state(false);
  if (!pokemon_nuevo.movimientos_nivel) pokemon_nuevo.movimientos_nivel = [];
  let timeoutMovNivel;
  function onInputMovNivel() {
    clearTimeout(timeoutMovNivel);
    if (queryMovNivel.length < 2) {
      resultsMovNivel = [];
      showDropdownMovNivel = false;
      return;
    }
    timeoutMovNivel = setTimeout(fetchResultsMovNivel, 300);
  }
  async function fetchResultsMovNivel() {
    let url = new URL(`http://localhost:8000/API-kachu/movimientos/`);
    url.search = new URLSearchParams({ nombre: queryMovNivel }).toString();
    const response = await fetch(url);
    if (response.ok) {
      resultsMovNivel = await response.json();
      showDropdownMovNivel = resultsMovNivel.length > 0;
    }
  }
  function selectResultMovNivel(result) {
    if (!pokemon_nuevo.movimientos_nivel.includes(result.id)) {
      pokemon_nuevo.movimientos_nivel = [
        ...pokemon_nuevo.movimientos_nivel,
        result.id,
      ];
    }
    queryMovNivel = "";
    showDropdownMovNivel = false;
  }
  function removeMovNivel(id) {
    pokemon_nuevo.movimientos_nivel = pokemon_nuevo.movimientos_nivel.filter(
      (m) => m !== id
    );
  }
  function handleBlurMovNivel() {
    setTimeout(() => (showDropdownMovNivel = false), 150);
  }
  function nombreMovNivelPorId(id) {
    const found = resultsMovNivel.find((m) => m.id === id);
    return found ? found.nombre : id;
  }

  // Generaciones
  let queryGeneracion = $state("");
  let resultsGeneracion = $state([]);
  let showDropdownGeneracion = $state(false);
  if (!pokemon_nuevo.generaciones) pokemon_nuevo.generaciones = [];
  let timeoutGeneracion;

  function onInputGeneracion() {
    clearTimeout(timeoutGeneracion);
    if (queryGeneracion.length < 1) {
      resultsGeneracion = [];
      showDropdownGeneracion = false;
      return;
    }
    timeoutGeneracion = setTimeout(fetchResultsGeneracion, 200);
  }

  function fetchResultsGeneracion() {
    resultsGeneracion = generaciones.filter(
      (g) =>
        (g.nombre.toLowerCase().includes(queryGeneracion.toLowerCase()) ||
          String(g.id).includes(queryGeneracion)) &&
        !pokemon_nuevo.generaciones.includes(g.id)
    );
    showDropdownGeneracion = resultsGeneracion.length > 0;
  }

  function selectResultGeneracion(result) {
    if (!pokemon_nuevo.generaciones.includes(result.id)) {
      pokemon_nuevo.generaciones = [...pokemon_nuevo.generaciones, result.id];
    }
    queryGeneracion = "";
    showDropdownGeneracion = false;
  }

  function removeGeneracion(id) {
    pokemon_nuevo.generaciones = pokemon_nuevo.generaciones.filter(
      (g) => g !== id
    );
  }

  function handleBlurGeneracion() {
    setTimeout(() => (showDropdownGeneracion = false), 150);
  }

  function nombreGeneracionPorId(id) {
    const found = resultsGeneracion.find((h) => h.id === id);
    return found ? found.nombre : id;
  }

  function parsearArrayNumeros(texto) {
    return texto
      .split(",")
      .map((x) => x.trim())
      .filter((x) => x !== "")
      .map(Number)
      .filter((x) => !isNaN(x));
  }

  function actualizarIdsDesdeInputs(
    generacionesTexto,
    tiposTexto,
    habilidadesTexto,
    movimientosHuevoTexto,
    movimientosMaquinaTexto,
    movimientosNivelTexto
  ) {
    pokemon_nuevo.generaciones = parsearArrayNumeros(generacionesTexto);
    pokemon_nuevo.tipos = parsearArrayNumeros(tiposTexto);
    pokemon_nuevo.habilidades = parsearArrayNumeros(habilidadesTexto);
    pokemon_nuevo.movimientos_huevo = parsearArrayNumeros(
      movimientosHuevoTexto
    );
    pokemon_nuevo.movimientos_maquina = parsearArrayNumeros(
      movimientosMaquinaTexto
    );
    pokemon_nuevo.movimientos_nivel = parsearArrayNumeros(
      movimientosNivelTexto
    );
  }

  onDestroy(() => {
    clearTimeout(timeout1);
    clearTimeout(timeout2);
  });
</script>

<Header />
<div class="contenedor-pokemon">
  <div class="tarjeta-pokemon">
    <form method="POST" action="?/crear" use:enhance>
      <div class="contenedor-flex">
        <div class="seccion-principal">
          <h2 class="nombre-pokemon">Creación de Pokémon</h2>
          <div class="imagen-container" style="margin-bottom: 16px;">
            <img
              class="imagen-pokemon"
              src="/imagenes/pokeball.png"
              alt="Nuevo Pokémon"
              style="opacity: 0.3;"
            />
          </div>
        </div>
        <div class="seccion-info">
          <div class="seccion-detalles">
            <div>
              <span class="etiqueta">Primer Pokémon Padre:</span>
              <input
                class="typeahead-input"
                type="text"
                bind:value={query1}
                oninput={onInput1}
                onblur={handleBlur1}
                placeholder="Buscar por nombre..."
                autocomplete="off"
              />
              <input
                type="hidden"
                name="primer_padre"
                value={pokemon_nuevo.primer_padre}
              />
              {#if showDropdown1}
                <div class="dropdown">
                  {#each results1 as result}
                    <div
                      class="dropdown-item"
                      role="button"
                      tabindex="0"
                      onmousedown={() => selectResult1(result)}
                    >
                      {result.nombre}
                    </div>
                  {/each}
                </div>
              {/if}
            </div>
            <div>
              <span class="etiqueta">Segundo Pokémon Padre:</span>
              <input
                class="typeahead-input"
                type="text"
                bind:value={query2}
                oninput={onInput2}
                onblur={handleBlur2}
                placeholder="Buscar por nombre..."
                autocomplete="off"
              />
              <input
                type="hidden"
                name="segundo_padre"
                value={pokemon_nuevo.segundo_padre}
              />
              {#if showDropdown2}
                <div class="dropdown">
                  {#each results2 as result}
                    <div
                      class="dropdown-item"
                      role="button"
                      tabindex="0"
                      onmousedown={() => selectResult2(result)}
                    >
                      {result.nombre}
                    </div>
                  {/each}
                </div>
              {/if}
            </div>
            <div>
              <span class="etiqueta">Altura:</span>
              <input
                class="typeahead-input"
                type="number"
                step="0.01"
                name="altura"
                bind:value={pokemon_nuevo.altura}
                placeholder="Ej: 0.8"
                autocomplete="off"
              />
            </div>
            <div>
              <span class="etiqueta">Peso:</span>
              <input
                class="typeahead-input"
                type="number"
                step="0.01"
                name="peso"
                bind:value={pokemon_nuevo.peso}
                placeholder="Ej: 20.0"
                autocomplete="off"
              />
            </div>
            <div class="detalles-item">
              <span class="etiqueta">Estadísticas:</span>
              <div class="valores-lista" style="flex-wrap: wrap; gap: 12px;">
                <div>
                  <label for="ataque">Ataque:</label>
                  <input
                    id="ataque"
                    class="typeahead-input"
                    type="number"
                    name="estadisticas.ataque"
                    bind:value={pokemon_nuevo.estadisticas.ataque}
                    placeholder="Ej: 62"
                    autocomplete="off"
                  />
                </div>
                <div>
                  <label for="defensa">Defensa:</label>
                  <input
                    id="defensa"
                    class="typeahead-input"
                    type="number"
                    name="estadisticas.defensa"
                    bind:value={pokemon_nuevo.estadisticas.defensa}
                    placeholder="Ej: 67"
                    autocomplete="off"
                  />
                </div>
                <div>
                  <label for="ataque_especial">Ataque Especial:</label>
                  <input
                    id="ataque_especial"
                    class="typeahead-input"
                    type="number"
                    name="estadisticas.ataque_especial"
                    bind:value={pokemon_nuevo.estadisticas.ataque_especial}
                    placeholder="Ej: 55"
                    autocomplete="off"
                  />
                </div>
                <div>
                  <label for="defensa_especial">Defensa Especial:</label>
                  <input
                    id="defensa_especial"
                    class="typeahead-input"
                    type="number"
                    name="estadisticas.defensa_especial"
                    bind:value={pokemon_nuevo.estadisticas.defensa_especial}
                    placeholder="Ej: 55"
                    autocomplete="off"
                  />
                </div>
                <div>
                  <label for="puntos_de_golpe">Puntos de Golpe:</label>
                  <input
                    id="puntos_de_golpe"
                    class="typeahead-input"
                    type="number"
                    name="estadisticas.puntos_de_golpe"
                    bind:value={pokemon_nuevo.estadisticas.puntos_de_golpe}
                    placeholder="Ej: 70"
                    autocomplete="off"
                  />
                </div>
                <div>
                  <label for="velocidad">Velocidad:</label>
                  <input
                    id="velocidad"
                    class="typeahead-input"
                    type="number"
                    name="estadisticas.velocidad"
                    bind:value={pokemon_nuevo.estadisticas.velocidad}
                    placeholder="Ej: 56"
                    autocomplete="off"
                  />
                </div>
              </div>
            </div>
            <div class="detalles-item">
              <span class="etiqueta">Generaciones:</span>
              <div style="flex:1;">
                <input
                  class="typeahead-input"
                  type="text"
                  bind:value={queryGeneracion}
                  oninput={onInputGeneracion}
                  onblur={handleBlurGeneracion}
                  placeholder="Buscar generación..."
                  autocomplete="off"
                />
                <input
                  type="hidden"
                  name="generaciones"
                  value={pokemon_nuevo.generaciones.join(",")}
                />
                {#if pokemon_nuevo.generaciones && pokemon_nuevo.generaciones.length > 0}
                  <div style="margin: 6px 0;">
                    {#each pokemon_nuevo.generaciones as id}
                      <span
                        style="display:inline-block; background:#eee; border-radius:4px; padding:2px 8px; margin-right:4px;"
                      >
                        {nombreGeneracionPorId(id)}
                        <button
                          type="button"
                          style="margin-left:4px;"
                          onclick={() => removeGeneracion(id)}>x</button
                        >
                      </span>
                    {/each}
                  </div>
                {/if}
                {#if showDropdownGeneracion}
                  <div class="dropdown">
                    {#each resultsGeneracion as result}
                      <div
                        class="dropdown-item"
                        role="button"
                        tabindex="0"
                        onmousedown={() => selectResultGeneracion(result)}
                      >
                        {result.nombre}
                      </div>
                    {/each}
                  </div>
                {/if}
              </div>
            </div>
            <div class="detalles-item">
              <span class="etiqueta">Tipos:</span>
              <div style="flex:1;">
                <input
                  class="typeahead-input"
                  type="text"
                  bind:value={queryTipo}
                  oninput={onInputTipo}
                  onblur={handleBlurTipo}
                  placeholder="Buscar tipo..."
                  autocomplete="off"
                />
                <input
                  type="hidden"
                  name="tipos"
                  value={pokemon_nuevo.tipos.join(",")}
                />
                {#if pokemon_nuevo.tipos && pokemon_nuevo.tipos.length > 0}
                  <div style="margin: 6px 0;">
                    {#each pokemon_nuevo.tipos as id}
                      <span
                        style="display:inline-block; background:#eee; border-radius:4px; padding:2px 8px; margin-right:4px;"
                      >
                        {nombreTipoPorId(id)}
                        <button
                          type="button"
                          style="margin-left:4px;"
                          onclick={() => removeTipo(id)}>x</button
                        >
                      </span>
                    {/each}
                  </div>
                {/if}
                {#if showDropdownTipo}
                  <div class="dropdown">
                    {#each resultsTipo as result}
                      <div
                        class="dropdown-item"
                        role="button"
                        tabindex="0"
                        onmousedown={() => selectResultTipo(result)}
                      >
                        {result.nombre}
                      </div>
                    {/each}
                  </div>
                {/if}
              </div>
            </div>
            <div class="detalles-item">
              <span class="etiqueta">Habilidades:</span>
              <div style="flex:1;">
                <input
                  class="typeahead-input"
                  type="text"
                  bind:value={queryHabilidad}
                  oninput={onInputHabilidad}
                  onblur={handleBlurHabilidad}
                  placeholder="Buscar habilidad..."
                  autocomplete="off"
                />
                <input
                  type="hidden"
                  name="habilidades"
                  value={pokemon_nuevo.habilidades.join(",")}
                />
                {#if pokemon_nuevo.habilidades && pokemon_nuevo.habilidades.length > 0}
                  <div style="margin: 6px 0;">
                    {#each pokemon_nuevo.habilidades as id}
                      <span
                        style="display:inline-block; background:#eee; border-radius:4px; padding:2px 8px; margin-right:4px;"
                      >
                        {nombreHabilidadPorId(id)}
                        <button
                          type="button"
                          style="margin-left:4px;"
                          onclick={() => removeHabilidad(id)}>x</button
                        >
                      </span>
                    {/each}
                  </div>
                {/if}
                {#if showDropdownHabilidad}
                  <div class="dropdown">
                    {#each resultsHabilidad as result}
                      <div
                        class="dropdown-item"
                        role="button"
                        tabindex="0"
                        onmousedown={() => selectResultHabilidad(result)}
                      >
                        {result.nombre}
                      </div>
                    {/each}
                  </div>
                {/if}
              </div>
            </div>
            <div class="detalles-item">
              <span class="etiqueta">Movimientos por huevo:</span>
              <div style="flex:1;">
                <input
                  class="typeahead-input"
                  type="text"
                  bind:value={queryMovHuevo}
                  oninput={onInputMovHuevo}
                  onblur={handleBlurMovHuevo}
                  placeholder="Buscar movimiento..."
                  autocomplete="off"
                />
                <input
                  type="hidden"
                  name="movimientos_huevo"
                  value={pokemon_nuevo.movimientos_huevo.join(",")}
                />
                {#if pokemon_nuevo.movimientos_huevo && pokemon_nuevo.movimientos_huevo.length > 0}
                  <div style="margin: 6px 0;">
                    {#each pokemon_nuevo.movimientos_huevo as id}
                      <span
                        style="display:inline-block; background:#eee; border-radius:4px; padding:2px 8px; margin-right:4px;"
                      >
                        {nombreMovHuevoPorId(id)}
                        <button
                          type="button"
                          style="margin-left:4px;"
                          onclick={() => removeMovHuevo(id)}>x</button
                        >
                      </span>
                    {/each}
                  </div>
                {/if}
                {#if showDropdownMovHuevo}
                  <div class="dropdown">
                    {#each resultsMovHuevo as result}
                      <div
                        class="dropdown-item"
                        role="button"
                        tabindex="0"
                        onmousedown={() => selectResultMovHuevo(result)}
                      >
                        {result.nombre}
                      </div>
                    {/each}
                  </div>
                {/if}
              </div>
            </div>
            <div class="detalles-item">
              <span class="etiqueta">Movimientos por máquina:</span>
              <div style="flex:1;">
                <input
                  class="typeahead-input"
                  type="text"
                  bind:value={queryMovMaquina}
                  oninput={onInputMovMaquina}
                  onblur={handleBlurMovMaquina}
                  placeholder="Buscar movimiento..."
                  autocomplete="off"
                />
                <input
                  type="hidden"
                  name="movimientos_maquina"
                  value={pokemon_nuevo.movimientos_maquina.join(",")}
                />
                {#if pokemon_nuevo.movimientos_maquina && pokemon_nuevo.movimientos_maquina.length > 0}
                  <div style="margin: 6px 0;">
                    {#each pokemon_nuevo.movimientos_maquina as id}
                      <span
                        style="display:inline-block; background:#eee; border-radius:4px; padding:2px 8px; margin-right:4px;"
                      >
                        {nombreMovMaquinaPorId(id)}
                        <button
                          type="button"
                          style="margin-left:4px;"
                          onclick={() => removeMovMaquina(id)}>x</button
                        >
                      </span>
                    {/each}
                  </div>
                {/if}
                {#if showDropdownMovMaquina}
                  <div class="dropdown">
                    {#each resultsMovMaquina as result}
                      <div
                        class="dropdown-item"
                        role="button"
                        tabindex="0"
                        onmousedown={() => selectResultMovMaquina(result)}
                      >
                        {result.nombre}
                      </div>
                    {/each}
                  </div>
                {/if}
              </div>
            </div>
            <div class="detalles-item">
              <span class="etiqueta">Movimientos por nivel:</span>
              <div style="flex:1;">
                <input
                  class="typeahead-input"
                  type="text"
                  bind:value={queryMovNivel}
                  oninput={onInputMovNivel}
                  onblur={handleBlurMovNivel}
                  placeholder="Buscar movimiento..."
                  autocomplete="off"
                />
                <input
                  type="hidden"
                  name="movimientos_nivel"
                  value={pokemon_nuevo.movimientos_nivel.join(",")}
                />
                {#if pokemon_nuevo.movimientos_nivel && pokemon_nuevo.movimientos_nivel.length > 0}
                  <div style="margin: 6px 0;">
                    {#each pokemon_nuevo.movimientos_nivel as id}
                      <span
                        style="display:inline-block; background:#eee; border-radius:4px; padding:2px 8px; margin-right:4px;"
                      >
                        {nombreMovNivelPorId(id)}
                        <button
                          type="button"
                          style="margin-left:4px;"
                          onclick={() => removeMovNivel(id)}>x</button
                        >
                      </span>
                    {/each}
                  </div>
                {/if}
                {#if showDropdownMovNivel}
                  <div class="dropdown">
                    {#each resultsMovNivel as result}
                      <div
                        class="dropdown-item"
                        role="button"
                        tabindex="0"
                        onmousedown={() => selectResultMovNivel(result)}
                      >
                        {result.nombre}
                      </div>
                    {/each}
                  </div>
                {/if}
              </div>
            </div>
            <div style="margin-top: 20px;">
              <button type="submit" style="margin-bottom:20px;">
                Crear Pokémon
              </button>
            </div>
          </div>
        </div>
      </div>
    </form>
    {#if form?.error}
      <div class="error-banner">{form.error}</div>
    {/if}
    {#if form?.success}
      <div class="success-banner">
        {form.success} Aqui tienes un link a su pagina:
        <a href="/pokemon/{form.pokemon.id}"> {form.pokemon.nombre} </a>
      </div>
    {/if}
  </div>
</div>
<Footer />

<style>
  .dropdown {
    position: absolute;

    max-height: 200px;
    overflow-y: auto;
    border: 1px solid #ccc;
    border-top: none;
    border-radius: 0 0 4px 4px;
    background: white;
    z-index: 1000;
    box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
  }

  .dropdown-item {
    padding: 8px;
    cursor: pointer;
    transition: background 0.2s;
  }

  .dropdown-item:hover {
    background: #f5f5f5;
  }

  .dropdown-item:active {
    background: #eee;
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
  .contenedor-pokemon {
    display: flex;
    justify-content: center;
    align-items: flex-start;
    padding: 20px;
    flex-direction: column;
  }

  .contenedor-flex {
    display: flex;
    flex-direction: row;
    width: 100%;
    gap: 20px;
  }

  .seccion-principal {
    flex: 1;
    display: flex;
    flex-direction: column;
    align-items: center;
  }

  .nombre-pokemon {
    font-size: 24px;
    font-weight: bold;
    margin: 0;
    margin-bottom: 12px;
  }

  .imagen-container {
    width: 100%;
    max-width: 300px;
    height: 200px;
    display: flex;
    justify-content: center;
    align-items: center;
    margin-bottom: 16px;
  }

  .imagen-pokemon {
    max-width: 100%;
    max-height: 100%;
    object-fit: contain;
  }

  .seccion-info {
    flex: 2;
    display: flex;
    flex-direction: column;
  }

  .seccion-detalles {
    flex: 1;
    display: flex;
    flex-direction: column;
    gap: 12px;
  }

  .etiqueta {
    font-weight: bold;
    margin-bottom: 4px;
    display: block;
  }

  .typeahead-input {
    padding: 8px;
    border: 1px solid #ccc;
    border-radius: 4px;
    width: 100%;
    box-sizing: border-box;
  }

  .detalles-item {
    display: flex;
    flex-direction: column;
  }

  .valores-lista {
    display: flex;
    flex-direction: row;
    flex-wrap: wrap;
    gap: 12px;
  }

  button[type="submit"] {
    background-color: #007bff;
    color: white;
    border: none;
    padding: 10px 20px;
    border-radius: 4px;
    cursor: pointer;
    font-size: 16px;
    transition: background 0.3s;
  }

  button[type="submit"]:hover {
    background-color: #0056b3;
  }

  .error-banner {
    background-color: #f8d7da;
    color: #721c24;
    padding: 10px;
    border-radius: 4px;
    margin-top: 10px;
  }

  .success-banner {
    background-color: #d4edda;
    color: #155724;
    padding: 10px;
    border-radius: 4px;
    margin-top: 10px;
  }
</style>
