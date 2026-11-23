# Proyecto de grafos

## Presentación

**Proyecto:** Sistema de defensa para el corredor estratégico “La derrota del
dictador General P. Tardo”.

Esta aplicación permite simular la defensa de un corredor mediante dos redes
de movimiento: una red elevada utilizada por las fuerzas humanas y un laberinto
por el que avanza el convoy enemigo. Utiliza grafos, estructuras propias,
algoritmos de caminos, planificación defensiva y una interfaz gráfica para
mostrar el estado de la simulación.

**Integrantes**

- Jaider León Diaz
- Joaquin Hoyos

**Presentado a:** Jeferson Arango Lopez

**Tecnologías:** Python, FastAPI, Pydantic, React, TypeScript, Vite, D3.js y
Tailwind CSS.

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
- [x] Interfaz moderna del centro de operaciones.
- [x] Cabecera, tarjetas métricas y controles visuales reutilizables.
- [x] Favicon personalizado de SismoLab AVL.

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

## Inicio rápido

Abrir dos terminales desde la carpeta raíz del proyecto.

### 1. Ejecutar el backend

```powershell
python -m venv backend\venv
.\backend\venv\Scripts\python.exe -m pip install -r backend\requirements.txt
.\backend\venv\Scripts\python.exe -m uvicorn backend.main:app --reload
```

API: <http://127.0.0.1:8000>

Documentación: <http://127.0.0.1:8000/docs>

### 2. Ejecutar el frontend

```powershell
cd frontend
npm ci
npm run dev
```

Interfaz: normalmente <http://localhost:5173>

Vite redirige las rutas `/api` al backend en el puerto `8000`.

### Resolver el puerto ocupado

`WinError 10013` significa que otra aplicación impide abrir el socket. Para
verificar qué proceso utiliza el puerto `8000`:

```powershell
Get-NetTCPConnection -LocalPort 8000 -State Listen
```

Si el proceso corresponde a una ejecución anterior de Uvicorn, detenerlo
por su PID:

```powershell
Stop-Process -Id <PID> -Force
```

Después ejecutar una sola vez:

```powershell
.\backend\venv\Scripts\python.exe -m uvicorn backend.main:app --reload --host 127.0.0.1 --port 8000
```

No repetir el comando de Uvicorn en varias terminales mientras la aplicación
ya se encuentre escuchando en el puerto `8000`.

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
│   ├── domain/                 # Scenario, ScenarioSummary, GraphKind, errores
│   ├── repository/             # escenario cargado en memoria
│   ├── schemas/                # un schema por cosa (vertex_ge, edge_gm, graph_ge, scenario...)
│   ├── service/
│   │   ├── graph/
│   │   │   ├── graph.py        # fachada GraphService
│   │   │   └── funciones/      # un archivo por función
│   │   └── scenario/
│   │       ├── scenario.py     # fachada ScenarioService
│   │       └── funciones/      # un archivo por función
│   ├── core/
│   │   ├── arista/             # EdgeMain, EdgeGE, EdgeGM
│   │   ├── grafo/
│   │   │   ├── graph.py        # Graph base (solo delega)
│   │   │   ├── graphGE.py
│   │   │   ├── graphGM.py
│   │   │   └── funciones/      # lógica del grafo: BFS, DFS, Dijkstra, validaciones...
│   │   ├── heap/               # MinHeap (cola de prioridad propia)
│   │   ├── queue/
│   │   ├── stack/
│   │   └── vertice/            # VertexMain, VertexGE, VertexGM
│   ├── utils/                  # funciones reutilizables (validadores numéricos)
│   └── tests/
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
- `service/`: fachadas de casos de uso; cada servicio tiene su carpeta con
  `funciones/` (un archivo por función) y la fachada solo las llama.
- `domain/`: entidades de aplicación (escenario, resumen) y sus errores.
- `repository/`: guarda el escenario cargado; los servicios lo reciben por constructor.
- `schemas/`: entradas y respuestas Pydantic, un archivo por cosa. Solo validan
  la forma del JSON; las reglas las aplican las clases del core.
- `core/`: estructuras de datos propias (vértices, aristas, grafos, cola, pila, heap).
  Cada grafo delega su lógica en `core/grafo/funciones/`.
- `utils/`: funciones reutilizables que no son estructuras de datos.
- `frontend/src/services/`: contiene las llamadas HTTP.
- `frontend/src/hooks/`: contiene estado y acciones reutilizables.
- `frontend/src/components/`: contiene presentación separada por responsabilidad.

## API actual

| Método | Ruta | Función |
| --- | --- | --- |
| `POST` | `/api/scenarios/load` | Valida, construye y guarda un escenario JSON |
| `GET` | `/api/scenarios/current` | Resumen del escenario cargado |
| `GET` | `/api/graphs/{ge\|gm}/vertices` | Lista vértices del grafo |
| `GET` | `/api/graphs/{ge\|gm}/vertices/{vertex_id}` | Consulta un vértice |
| `GET` | `/api/graphs/{ge\|gm}/vertices/{vertex_id}/neighbors` | Lista vecinos |
| `GET` | `/api/graphs/{ge\|gm}/edges` | Lista aristas |
| `GET` | `/api/graphs/{ge\|gm}/traversals/breadth-first?start={id}` | Ejecuta BFS |
| `GET` | `/api/graphs/{ge\|gm}/traversals/depth-first?start={id}` | Ejecuta DFS |

Los grafos se construyen al cargar el escenario (ya no se crean vértices ni
aristas a mano). El escenario se conserva en memoria y se pierde al reiniciar
el backend; sin escenario cargado, las consultas de grafos responden 409.

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

1. Añadir un schema por cosa en `backend/schemas/` (importando los de sus partes).
2. Poner las reglas de cada entidad en su clase del core, y la lógica de los
   grafos en `backend/core/grafo/funciones/`.
3. Coordinar el caso de uso en `backend/service/<servicio>/funciones/` y
   exponerlo desde la fachada `backend/service/<servicio>/<servicio>.py`.
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
