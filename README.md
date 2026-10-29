# Proyecto de grafos

Aplicación para crear y visualizar grafos dirigidos. El backend usa FastAPI y
mantiene el grafo en memoria; el frontend está hecho con React, TypeScript,
Tailwind CSS y D3.js.

## Requisitos

- Python 3.10 o posterior.
- Node.js y npm.

## Ejecutar en Windows

Abre dos terminales en la carpeta raíz del proyecto.

### 1. Backend

En la primera terminal, crea y activa el entorno virtual e instala dependencias:

```powershell
cd backend
py -m venv venv
.\venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
python -m uvicorn main:app --reload
```

La API estará disponible en <http://127.0.0.1:8000> y su documentación
interactiva en <http://127.0.0.1:8000/docs>.

Si PowerShell bloquea la activación del entorno virtual, puedes invocar sus
ejecutables directamente desde la raíz del proyecto:

```powershell
.\backend\venv\Scripts\python.exe -m pip install -r backend\requirements.txt
.\backend\venv\Scripts\python.exe -m uvicorn backend.main:app --reload
```

### 2. Frontend

En la segunda terminal, desde la raíz del proyecto:

```powershell
cd frontend
npm ci
npm run dev
```

Vite muestra la dirección local en la terminal (normalmente
<http://localhost:5173>). El proxy de desarrollo reenvía `/api` a
<http://127.0.0.1:8000>, por lo que el backend debe estar activo para usar la
interfaz.

## Comandos del frontend

Ejecuta estos comandos desde `frontend`:

```powershell
npm run build
npm run lint
npm run preview
```

## Funcionalidades

- Crear y consultar vértices y aristas dirigidas con peso.
- Explorar visualmente el grafo con D3.js, arrastrar nodos y seleccionar un
  vértice para ver su estado, grados y conexiones entrantes y salientes.
- Ejecutar recorridos BFS (anchura) y DFS (profundidad).
- Consultar y probar la API con Swagger UI en `/docs`.

Los datos se guardan en memoria: se pierden al reiniciar el backend.

## Organización

```text
backend/
  controllers/  Rutas y manejo de errores HTTP
  core/         Estructuras y lógica base del grafo
  schemas/      Modelos de entrada y salida de la API
  service/      Lógica de aplicación
frontend/
  src/
    components/ Componentes reutilizables
    hooks/      Estado y acciones del grafo
    pages/      Vistas
    services/   Cliente HTTP
    types/      Tipos de datos
```
