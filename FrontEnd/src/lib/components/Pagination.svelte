<script>
  let { currentPage, hasMore, onPrev, onNext } = $props();
</script>

<div class="pagination">
  {#if currentPage > 0}
    <button onclick={onPrev} class="pagination-btn"> ← Anterior </button>
  {/if}

  <span class="page-info">
    Página {currentPage + 1}
  </span>

  {#if hasMore}
    <button onclick={onNext} class="pagination-btn"> Siguiente → </button>
  {/if}
</div>
