# API Pokémon

Una API RESTful que permite acceder a información detallada sobre Pokémon, incluyendo datos como nombre, tipo, estadísticas y movimientos.

## 🚀 Instalación

1. Clona el repositorio:

   ```bash
   git clone https://github.com/Nehuenkend/API_pokemon.git
   cd API_pokemon
   ```

2. Instala las dependencias:

   ```bash
   npm install
   ```

3. Inicia el servidor:

   ```bash
   npm start
   ```

La API estará disponible en `http://localhost:3000`.

## 📚 Endpoints disponibles

- `GET /pokemon`: Obtiene una lista de todos los Pokémon.
- `GET /pokemon/:id`: Obtiene información detallada de un Pokémon por su ID.
- `GET /types`: Obtiene una lista de todos los tipos de Pokémon.
- `GET /types/:type`: Obtiene una lista de Pokémon por tipo.

## 🧪 Pruebas

Para ejecutar las pruebas unitarias:

```bash
npm test
```

## 🛠️ Tecnologías utilizadas

- Node.js
- Express
- Jest (para pruebas)

## 📄 Licencia

Este proyecto está licenciado bajo la Licencia MIT.

