import { error } from "@sveltejs/kit";

export async function load({ url }) {
  const page = parseInt(url.searchParams.get("page") || "0");
  const nombre = url.searchParams.get("nombre") || "";
  const tipo = url.searchParams.get("tipo") || "";

  const pageSize = 20;
  const offset = page * pageSize;

  let apiUrl = new URL(`http://localhost:8000/API-kachu/pokemones`);
  apiUrl.searchParams.set("limit", pageSize.toString());
  apiUrl.searchParams.set("offset", offset.toString());

  if (nombre) {
    apiUrl.searchParams.set("nombre", nombre);
  }
  if (tipo) {
    apiUrl.searchParams.set("tipo", tipo);
  }

  const response = await fetch(apiUrl);
  if (!response.ok) {
    error(
      response.status,
      `Error al cargar los pokemones: ${response.statusText}`
    );
  }
  const pokemones = await response.json();

  const hasMore = pokemones.length === pageSize;

  return {
    pokemones: pokemones,
    currentPage: page,
    pageSize: pageSize,
    hasMore: hasMore,
    filtros: {
      nombre,
      tipo,
    },
  };
}
