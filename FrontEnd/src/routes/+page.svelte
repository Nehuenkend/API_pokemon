<script>
  import Footer from "$lib/components/Footer.svelte";
</script>

<div class="img-header"></div>

<div>
  <div class="info-pag">
    <p class="titulo">Bienvenidos a la pagina de API-Kachu</p>
    <p class="info">
      En esta pagina van a poder encontrar una amplia informacion sobre sus
      pokemones preferidos, navegando por cualquiera de las siguentes ventanas
    </p>
    <div class="contenido">
      <div class="info-mov">
        <p class="titulo-mov">Movimiento</p>
        <p class="descripcion">
          Explora todos los movimientos disponibles para tus Pokémon. Filtra por
          tipo, potencia o efecto para encontrar las mejores estrategias de
          batalla.
        </p>
      </div>
      <div class="info-poke">
        <p class="titulo-poke">Pokemones</p>
        <p class="descripcion">
          Explora información detallada de cualquier Pokémon: sus stats,
          movimientos aprendibles, tipos, evoluciones y generaciones a las que
          pertenece. ¿Te gustaría diseñar tu propio Pokémon? Usa nuestra
          herramienta de creación para inventar criaturas con características
          únicas.
        </p>
      </div>
      <div class="info-equipo">
        <p class="titulo-equipo">Equipos</p>
        <p class="descripcion">
          Construye equipos estratégicos: analiza debilidades, cubre sinergias y
          optimiza tu lineup para torneos.
        </p>
      </div>
    </div>
  </div>
</div>

<Footer />

<style>
  @import "$lib/css/styles.css";
</style>
