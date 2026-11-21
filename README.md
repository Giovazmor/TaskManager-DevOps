# TaskManager-DevOps

Sistema web para la gestión de tareas de TechSolutions, desarrollado aplicando las fases del ciclo DevOps con GitHub.

## Funcionalidades

| Código | Funcionalidad | Endpoint |
|--------|---------------|----------|
| RF01 | Registrar tareas | `POST /api/tareas` |
| RF02 | Consultar tareas | `GET /api/tareas` |
| RF03 | Editar tareas | `PUT /api/tareas/<id>` |
| RF04 | Eliminar tareas | `DELETE /api/tareas/<id>` |
| RF05 | Cambiar estado (Pendiente, En proceso, Terminada) | `PATCH /api/tareas/<id>/estado` |
| RF06 | Asignar prioridad (Alta, Media, Baja) | campo `prioridad` en RF01/RF03 |

## Tecnologías

Flask · SQLite · HTML/CSS/JavaScript · pytest · GitHub Actions · Render

## Ejecutar en local

```bash
git clone https://github.com/USUARIO/TaskManager-DevOps.git
cd TaskManager-DevOps
python -m venv .venv && source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -r requirements.txt
python app.py        # http://127.0.0.1:5000
```

## Pruebas

```bash
pytest -v
```

## Flujo de trabajo

- Ramas `feature/*` por funcionalidad, Pull Request hacia `main` con al menos una revisión.
- CI (`.github/workflows/ci.yml`): ejecuta pytest en cada push y PR a `main`.
- Entrega (`.github/workflows/entrega.yml`): al publicar un Release genera el artefacto `TaskManager-v1`.
- Despliegue: Render (`render.yaml`), comando de inicio `gunicorn app:app`, health check en `/health`.
