export async function load({ fetch, url }) {
  const nombre = url.searchParams.get("nombre") || "";
  const pageSize = 20;
  const page = Number(url.searchParams.get("page") || 0);
  const offset = page * pageSize;

  let apiUrl = new URL(`http://localhost:8000/API-kachu/movimientos/`);
  apiUrl.searchParams.set("limit", pageSize.toString());
  apiUrl.searchParams.set("offset", offset.toString());

  if (nombre) {
    apiUrl.searchParams.set("nombre", nombre);
  }

  const response = await fetch(apiUrl);
  if (!response.ok) {
    error(
      response.status,
      `Error al cargar los movimientos: ${response.statusText}`
    );
  }

  const movimientos = await response.json();
  const hasMore = movimientos.length === pageSize;

  return {
    movimientos,
    pageSize,
    hasMore,
    currentPage: page,
    filtros: { nombre, page },
  };
}
