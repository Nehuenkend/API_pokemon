import { fail } from "@sveltejs/kit";

export async function load({ params }) {
  let url_generaciones = new URL(
    "http://localhost:8000/API-kachu/generaciones"
  );
  const response_generaciones = await fetch(url_generaciones);
  if (!response_generaciones.ok) {
    throw new Error("No se pudieron cargar las generaciones");
  }
  let generaciones = await response_generaciones.json();

  return {
    generaciones,
  };
}

export const actions = {
  crear: async ({ request }) => {
    const data = await request.formData();

    const payload = {
      altura: parseFloat(data.get("altura")),
      peso: parseFloat(data.get("peso")),
      generaciones: data.get("generaciones")
        ? [parseInt(data.get("generaciones"))]
        : [],
      tipos: data.get("tipos") ? [parseInt(data.get("tipos"))] : [],
      habilidades: data.get("habilidades")
        ? [parseInt(data.get("habilidades"))]
        : [],
      estadisticas: {
        ataque: parseInt(data.get("estadisticas.ataque")),
        defensa: parseInt(data.get("estadisticas.defensa")),
        ataque_especial: parseInt(data.get("estadisticas.ataque_especial")),
        defensa_especial: parseInt(data.get("estadisticas.defensa_especial")),
        puntos_de_golpe: parseInt(data.get("estadisticas.puntos_de_golpe")),
        velocidad: parseInt(data.get("estadisticas.velocidad")),
      },
      movimientos_huevo: data.get("movimientos_huevo")
        ? [parseInt(data.get("movimientos_huevo"))]
        : [],
      movimientos_maquina: data.get("movimientos_maquina")
        ? [parseInt(data.get("movimientos_maquina"))]
        : [],
      movimientos_nivel: data.get("movimientos_nivel")
        ? [parseInt(data.get("movimientos_nivel"))]
        : [],
      primer_padre: data.get("primer_padre")
        ? [parseInt(data.get("primer_padre"))]
        : [],
      segundo_padre: data.get("segundo_padre")
        ? [parseInt(data.get("segundo_padre"))]
        : [],
    };

    let url = new URL(`http://localhost:8000/API-kachu/pokemones`);

    const response = await fetch(url, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(payload),
    });

    if (!response.ok) {
      const errorData = await response.json();
      return fail(400, {
        error:
          errorData.detail?.[0]?.msg ||
          errorData.detail ||
          errorData.message ||
          "Completa todos los campos para empezar a crear a tu Pokemon !",
      });
    }

    let pokemon = await response.json();

    return { success: "Pokemon creado correctamente!", pokemon };
  },
};
