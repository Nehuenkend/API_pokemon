import { error } from "@sveltejs/kit";

export async function load({ params }) {
  try {
    const response = await fetch(
      `http://localhost:8000/API-kachu/pokemones/${params.id}`
    );
    if (!response.ok) {
      throw error(response.status, "No se pudo cargar el pokemon");
    }
    const pokemon = await response.json();
    return { pokemon };
  } catch (err) {
    throw error(500, "Error al conectar con la API");
  }
}
