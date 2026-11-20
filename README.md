# Proyecto de grafos

Aplicación para la simulación de defensa descrita en
`ProyectoGrafos.pdf`. El sistema combina FastAPI, React, TypeScript y D3.js.

## Estado actual

### Completado

- [x] Backend ejecutable con FastAPI.
- [x] Frontend ejecutable con React, TypeScript y Vite.
- [x] Creación y consulta de vértices.
- [x] Creación y consulta de aristas dirigidas con peso.
- [x] Visualización y selección de vértices.
- [x] Recorridos BFS y DFS.
- [x] Entidades base de vértices y aristas GE/GM.
- [x] Validación centralizada de valores numéricos e identificadores.
- [x] Carga y validación inicial de escenarios JSON.
- [x] Cálculo del menor tiempo entre entrada y salida de GM.

### Pendiente

- [ ] Integrar el escenario cargado con las estructuras visuales GE/GM.
- [ ] Construir el árbol de expansión mínima.
- [ ] Seleccionar torres por cobertura y costo.
- [ ] Implementar soldados, convoy y unidades enemigas.
- [ ] Implementar combate y cálculo de peligro.
- [ ] Implementar navegación reactiva.
- [ ] Implementar puentes dinámicos y reconstrucción.
- [ ] Implementar transporte aéreo y terrestre.
- [ ] Implementar presupuesto, reservas y reloj lógico.
- [ ] Implementar condiciones de finalización.
- [ ] Añadir dos escenarios JSON documentados.
- [ ] Añadir manual técnico y manual de usuario.

## Tecnologías

| Capa | Tecnologías |
| --- | --- |
| Backend | Python 3.10+, FastAPI, Pydantic |
| Frontend | React 19, TypeScript, Vite, D3.js, Tailwind CSS |
| Pruebas backend | `unittest` |
| Pruebas frontend | Build y ESLint |

## Inicio rápido

### Backend

Desde la raíz:

```powershell
py -m venv backend\venv
backend\venv\Scripts\python.exe -m pip install -r backend\requirements.txt
backend\venv\Scripts\python.exe -m uvicorn backend.main:app --reload
```

API: <http://127.0.0.1:8000>

Documentación: <http://127.0.0.1:8000/docs>

También puede ejecutarse desde `backend`:

```powershell
cd backend
py -m uvicorn main:app --reload
```

### Frontend

Desde la raíz:

```powershell
cd frontend
npm ci
npm run dev
```

Interfaz: normalmente <http://localhost:5173>

Vite redirige las rutas `/api` al backend en el puerto `8000`.

## Comandos de desarrollo

### Frontend

```powershell
cd frontend
npm run build
npm run lint
npm run preview
```

### Backend

Desde la raíz:

```powershell
python -m unittest discover -s backend/tests -p "test_*.py" -v
```

## Organización del repositorio

```text
Proyecto-grafos/
├── ProyectoGrafos.pdf
├── README.md
├── scenarios/
│   └── ejemplo-minimo.json
├── backend/
│   ├── main.py
│   ├── requirements.txt
│   ├── controllers/
│   │   ├── error_handler.py
│   │   ├── graph_controller.py
│   │   └── scenario_controller.py
│   ├── domain/
│   │   └── scenario.py
│   ├── schemas/
│   │   ├── graph_schemas.py
│   │   └── scenario_schemas.py
│   ├── service/
│   │   ├── graph.py
│   │   └── scenario.py
│   ├── core/
│   │   ├── arista/
│   │   ├── grafo/
│   │   ├── queue/
│   │   ├── stack/
│   │   ├── validaciones/
│   │   └── vertice/
│   └── tests/
│       ├── test_graph_service.py
│       └── test_scenario_service.py
└── frontend/
    └── src/
        ├── components/
        │   ├── forms/
        │   └── graph/
        ├── hooks/
        ├── pages/
        ├── services/
        └── types/
```

### Responsabilidades

- `controllers/`: recibe peticiones HTTP y transforma respuestas.
- `service/`: coordina casos de uso y conserva la lógica de aplicación fuera de FastAPI.
- `domain/`: contiene reglas e invariantes independientes del transporte HTTP.
- `schemas/`: define entradas y respuestas Pydantic.
- `core/`: contiene estructuras propias, vértices, aristas y validadores.
- `frontend/src/services/`: contiene las llamadas HTTP.
- `frontend/src/hooks/`: contiene estado y acciones reutilizables.
- `frontend/src/components/`: contiene presentación separada por responsabilidad.

## API actual

| Método | Ruta | Función |
| --- | --- | --- |
| `POST` | `/api/vertices` | Crea un vértice |
| `GET` | `/api/vertices` | Lista vértices |
| `GET` | `/api/vertices/{vertex_id}` | Consulta un vértice |
| `POST` | `/api/edges` | Crea una arista |
| `GET` | `/api/edges` | Lista aristas |
| `GET` | `/api/vertices/{vertex_id}/neighbors` | Lista vecinos |
| `GET` | `/api/traversals/breadth-first?start={id}` | Ejecuta BFS |
| `GET` | `/api/traversals/depth-first?start={id}` | Ejecuta DFS |
| `POST` | `/api/scenarios/load` | Valida y carga un escenario JSON |

El grafo operativo actual se conserva en memoria y se reinicia al reiniciar el
backend.

## Formato inicial de escenario

El usuario selecciona el archivo desde la interfaz. El JSON no usa rutas fijas
en el servidor. El ejemplo completo está en
[scenarios/ejemplo-minimo.json](./scenarios/ejemplo-minimo.json).

Campos principales:

- `name`: nombre del escenario.
- `ge.vertices`: posiciones humanas.
- `ge.edges`: caminos o puentes elevados.
- `gm.vertices`: intersecciones del laberinto.
- `gm.edges`: corredores del laberinto.
- `base_id`: identificador único de la base GE.
- `entry_id`: identificador único de entrada GM.
- `exit_id`: identificador único de salida GM.
- `parameters`: límite de torres, peligro, resistencia, presupuesto y tiempo.
- `convoy`: cantidades iniciales de tanques, camiones y robots.

Invariantes validadas actualmente:

- Identificadores únicos dentro de cada grafo.
- GE tiene exactamente una base.
- GM tiene exactamente una entrada y una salida distintas.
- Las aristas apuntan a vértices existentes.
- Las aristas no forman bucles de un vértice consigo mismo.
- Las coordenadas GE son positivas y finitas.
- Las coordenadas GM son finitas.
- Los puentes requieren resistencia máxima.
- Los caminos no pueden contener resistencia.
- Al menos un medio de transporte debe existir en cada arista GE.
- GM contiene una ruta entre entrada y salida.

## Convenciones para continuar

### Backend

1. Añadir modelos de entrada en `backend/schemas/`.
2. Añadir reglas independientes de HTTP en `backend/domain/`.
3. Coordinar el caso de uso en `backend/service/`.
4. Exponer rutas pequeñas en `backend/controllers/`.
5. Registrar la ruta en `backend/main.py`.
6. Añadir pruebas en `backend/tests/`.

### Frontend

1. Añadir contratos TypeScript en `frontend/src/types/`.
2. Añadir llamadas HTTP en `frontend/src/services/`.
3. Mantener estado compartido en `frontend/src/hooks/`.
4. Crear componentes pequeños en `frontend/src/components/`.
5. Usar páginas solamente para composición de vistas.

## Registro de cambios

Al completar una fase, actualizar esta sección con:

1. Fecha o número de fase.
2. Archivos añadidos o modificados.
3. Funcionalidad agregada.
4. Comandos utilizados para verificarla.

Ejemplo:

```text
Fase 1 - Carga de escenarios
- Añadido: backend/schemas/scenario_schemas.py
- Añadido: backend/domain/scenario.py
- Añadido: backend/service/scenario.py
- Añadido: backend/controllers/scenario_controller.py
- Añadido: frontend/src/components/forms/ScenarioLoader.tsx
- Verificado: python -m unittest discover -s backend/tests -p "test_*.py" -v
- Verificado: npm run build
- Verificado: npm run lint
```
