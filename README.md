# API Pokémon

Este repositorio contiene dos carpetas principales:

- **Backend**: API construida con FastAPI, SQLModel y migraciones con Alembic.  
- **Frontend**: Proyecto frontend hecho con Svelte.

---

## 🚀 Instalación y ejecución

### Backend

1. Clona el repositorio:

   ```bash
   git clone https://github.com/Nehuenkend/API_pokemon.git
   cd API_pokemon/backend
   ```

2. Crea y activa un entorno virtual de Python (recomendado):

   ```bash
   python -m venv .venv
   source .venv/bin/activate   # En Linux/macOS
   .\.venv\Scripts\activate  # En Windows PowerShell
   ```

3. Instala las dependencias:

   ```bash
   pip install -r requirements.txt
   ```

4. Ejecuta las migraciones con Alembic para crear la base de datos y las tablas:

   ```bash
   alembic upgrade head
   ```

5. Inicia el servidor FastAPI:

   ```bash
   uvicorn main:app --reload
   ```

6. La API backend estará disponible en `http://localhost:8000`.

---

### Frontend (Svelte)

1. Abre otra terminal y navega a la carpeta del frontend:

   ```bash
   cd ../frontend
   ```

2. Si no tienes creado el proyecto Svelte, puedes crearlo con:

   ```bash
   npx create-svelte@latest
   ```

   (Sigue las instrucciones para configurar el proyecto)

3. Instala las dependencias del frontend:

   ```bash
   npm install
   ```

4. Inicia el servidor de desarrollo:

   ```bash
   npm run dev -- --open
   ```

5. El frontend estará disponible usualmente en `http://localhost:5173`.

---

## 📚 Uso

- El backend sirve la API REST para consumir datos de Pokémon.  
- El frontend consume esa API para mostrar la información en una interfaz amigable.

---

## 🛠️ Tecnologías utilizadas

- Backend: FastAPI, SQLModel, Alembic  
- Frontend: Svelte, Node.js

---

## 📄 Licencia

Este proyecto está licenciado bajo la Licencia MIT.


