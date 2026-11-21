"""TaskManager - Sistema web para la gestión de tareas (Flask + SQLite)."""
import os
import sqlite3

from flask import Flask, g, jsonify, render_template, request

ESTADOS = ("Pendiente", "En proceso", "Terminada")
PRIORIDADES = ("Alta", "Media", "Baja")

SCHEMA = """
CREATE TABLE IF NOT EXISTS tareas (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nombre TEXT NOT NULL,
    descripcion TEXT NOT NULL DEFAULT '',
    estado TEXT NOT NULL DEFAULT 'Pendiente',
    prioridad TEXT NOT NULL DEFAULT 'Media'
);
"""


def validar_tarea(datos, parcial=False):
    """Valida los datos de una tarea. Devuelve (datos_limpios, error)."""
    if not isinstance(datos, dict):
        return None, "El cuerpo de la petición debe ser un objeto JSON."
    limpio = {}

    if "nombre" in datos or not parcial:
        nombre = str(datos.get("nombre", "")).strip()
        if not nombre:
            return None, "El nombre de la tarea es obligatorio."
        if len(nombre) > 100:
            return None, "El nombre no puede exceder 100 caracteres."
        limpio["nombre"] = nombre

    if "descripcion" in datos:
        limpio["descripcion"] = str(datos["descripcion"] or "").strip()

    if "estado" in datos:
        if datos["estado"] not in ESTADOS:
            return None, "Estado inválido. Use: " + ", ".join(ESTADOS) + "."
        limpio["estado"] = datos["estado"]

    if "prioridad" in datos:
        if datos["prioridad"] not in PRIORIDADES:
            return None, "Prioridad inválida. Use: " + ", ".join(PRIORIDADES) + "."
        limpio["prioridad"] = datos["prioridad"]

    return limpio, None


def create_app(db_path=None):
    app = Flask(__name__)
    app.config["DATABASE"] = db_path or os.environ.get(
        "DATABASE_PATH", os.path.join(app.root_path, "tasks.db")
    )

    def get_db():
        if "db" not in g:
            g.db = sqlite3.connect(app.config["DATABASE"])
            g.db.row_factory = sqlite3.Row
        return g.db

    @app.teardown_appcontext
    def close_db(_exc):
        db = g.pop("db", None)
        if db is not None:
            db.close()

    with app.app_context():
        get_db().executescript(SCHEMA)

    def fila_a_dict(fila):
        return {k: fila[k] for k in fila.keys()}

    def obtener(tarea_id):
        return get_db().execute(
            "SELECT * FROM tareas WHERE id = ?", (tarea_id,)
        ).fetchone()

    @app.get("/")
    def index():
        return render_template("index.html")

    @app.get("/health")
    def health():
        get_db().execute("SELECT 1")
        return jsonify(status="ok")

    # RF02 - Consultar tareas
    @app.get("/api/tareas")
    def listar():
        filas = get_db().execute("SELECT * FROM tareas ORDER BY id DESC").fetchall()
        return jsonify([fila_a_dict(f) for f in filas])

    # RF01 + RF06 - Registrar tarea (con prioridad)
    @app.post("/api/tareas")
    def crear():
        datos, error = validar_tarea(request.get_json(silent=True))
        if error:
            return jsonify(error=error), 400
        db = get_db()
        cur = db.execute(
            "INSERT INTO tareas (nombre, descripcion, estado, prioridad) "
            "VALUES (?, ?, ?, ?)",
            (
                datos["nombre"],
                datos.get("descripcion", ""),
                datos.get("estado", "Pendiente"),
                datos.get("prioridad", "Media"),
            ),
        )
        db.commit()
        return jsonify(fila_a_dict(obtener(cur.lastrowid))), 201

    # RF03 - Editar tarea
    @app.put("/api/tareas/<int:tarea_id>")
    def editar(tarea_id):
        if obtener(tarea_id) is None:
            return jsonify(error="Tarea no encontrada."), 404
        datos, error = validar_tarea(request.get_json(silent=True), parcial=True)
        if error:
            return jsonify(error=error), 400
        if datos:
            db = get_db()
            sets = ", ".join(f"{campo} = ?" for campo in datos)
            db.execute(
                f"UPDATE tareas SET {sets} WHERE id = ?",
                (*datos.values(), tarea_id),
            )
            db.commit()
        return jsonify(fila_a_dict(obtener(tarea_id)))

    # RF05 - Cambiar estado
    @app.patch("/api/tareas/<int:tarea_id>/estado")
    def cambiar_estado(tarea_id):
        if obtener(tarea_id) is None:
            return jsonify(error="Tarea no encontrada."), 404
        cuerpo = request.get_json(silent=True)
        if not isinstance(cuerpo, dict) or "estado" not in cuerpo:
            return jsonify(error="Debe enviar el campo 'estado'."), 400
        datos, error = validar_tarea({"estado": cuerpo["estado"]}, parcial=True)
        if error:
            return jsonify(error=error), 400
        db = get_db()
        db.execute(
            "UPDATE tareas SET estado = ? WHERE id = ?", (datos["estado"], tarea_id)
        )
        db.commit()
        return jsonify(fila_a_dict(obtener(tarea_id)))

    # RF04 - Eliminar tarea
    @app.delete("/api/tareas/<int:tarea_id>")
    def eliminar(tarea_id):
        if obtener(tarea_id) is None:
            return jsonify(error="Tarea no encontrada."), 404
        db = get_db()
        db.execute("DELETE FROM tareas WHERE id = ?", (tarea_id,))
        db.commit()
        return "", 204

    return app


app = create_app()

if __name__ == "__main__":
    app.run(debug=True)
