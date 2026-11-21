import os
import sys

import pytest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app import create_app, validar_tarea  # noqa: E402


@pytest.fixture()
def client(tmp_path):
    app = create_app(str(tmp_path / "test.db"))
    app.config["TESTING"] = True
    return app.test_client()


def crear(client, **extra):
    datos = {"nombre": "Realizar actividad DevOps", "descripcion": "Detalle", **extra}
    return client.post("/api/tareas", json=datos)


# ---------- Unitarias: validación ----------
def test_validar_tarea_valida():
    datos, error = validar_tarea({"nombre": "  Tarea  ", "prioridad": "Alta"})
    assert error is None
    assert datos["nombre"] == "Tarea"
    assert datos["prioridad"] == "Alta"


def test_validar_tarea_sin_nombre():
    _, error = validar_tarea({"nombre": "   "})
    assert error == "El nombre de la tarea es obligatorio."


def test_validar_estado_invalido():
    _, error = validar_tarea({"nombre": "x", "estado": "Otro"})
    assert "Estado inválido" in error


def test_validar_prioridad_invalida():
    _, error = validar_tarea({"nombre": "x", "prioridad": "Urgente"})
    assert "Prioridad inválida" in error


def test_validar_nombre_largo():
    _, error = validar_tarea({"nombre": "a" * 101})
    assert "100" in error


# ---------- CP01 / RF01: registrar ----------
def test_cp01_registrar_tarea(client):
    resp = crear(client, prioridad="Alta")
    assert resp.status_code == 201
    cuerpo = resp.get_json()
    assert cuerpo["nombre"] == "Realizar actividad DevOps"
    assert cuerpo["estado"] == "Pendiente"
    assert cuerpo["id"] == 1


# ---------- CP02: registrar sin nombre ----------
def test_cp02_registrar_sin_nombre(client):
    resp = client.post("/api/tareas", json={"descripcion": "sin nombre"})
    assert resp.status_code == 400
    assert "obligatorio" in resp.get_json()["error"]


def test_registrar_sin_descripcion_es_valido(client):
    resp = client.post("/api/tareas", json={"nombre": "Solo nombre"})
    assert resp.status_code == 201
    assert resp.get_json()["descripcion"] == ""


def test_registrar_cuerpo_no_json(client):
    resp = client.post("/api/tareas", data="no es json")
    assert resp.status_code == 400


# ---------- CP03 / RF02: consultar ----------
def test_cp03_consultar_tareas(client):
    assert client.get("/api/tareas").get_json() == []
    crear(client, nombre="Uno")
    crear(client, nombre="Dos")
    lista = client.get("/api/tareas").get_json()
    assert [t["nombre"] for t in lista] == ["Dos", "Uno"]


# ---------- CP04 / RF03: editar ----------
def test_cp04_editar_tarea(client):
    tarea_id = crear(client).get_json()["id"]
    resp = client.put(
        f"/api/tareas/{tarea_id}",
        json={"nombre": "Nombre nuevo", "descripcion": "Otra"},
    )
    assert resp.status_code == 200
    assert resp.get_json()["nombre"] == "Nombre nuevo"
    assert resp.get_json()["descripcion"] == "Otra"


def test_editar_tarea_inexistente(client):
    resp = client.put("/api/tareas/999", json={"nombre": "x"})
    assert resp.status_code == 404


def test_editar_con_nombre_vacio_falla(client):
    tarea_id = crear(client).get_json()["id"]
    resp = client.put(f"/api/tareas/{tarea_id}", json={"nombre": ""})
    assert resp.status_code == 400


# ---------- CP05 / RF04: eliminar ----------
def test_cp05_eliminar_tarea(client):
    tarea_id = crear(client).get_json()["id"]
    assert client.delete(f"/api/tareas/{tarea_id}").status_code == 204
    assert client.get("/api/tareas").get_json() == []


def test_eliminar_tarea_inexistente(client):
    assert client.delete("/api/tareas/999").status_code == 404


# ---------- CP06 / RF05: cambiar estado ----------
@pytest.mark.parametrize("estado", ["Pendiente", "En proceso", "Terminada"])
def test_cp06_cambiar_estado(client, estado):
    tarea_id = crear(client).get_json()["id"]
    resp = client.patch(f"/api/tareas/{tarea_id}/estado", json={"estado": estado})
    assert resp.status_code == 200
    assert resp.get_json()["estado"] == estado
    lista = client.get("/api/tareas").get_json()
    assert lista[0]["estado"] == estado


def test_cambiar_estado_invalido(client):
    tarea_id = crear(client).get_json()["id"]
    resp = client.patch(f"/api/tareas/{tarea_id}/estado", json={"estado": "Hecho"})
    assert resp.status_code == 400


def test_cambiar_estado_sin_campo(client):
    tarea_id = crear(client).get_json()["id"]
    resp = client.patch(f"/api/tareas/{tarea_id}/estado", json={})
    assert resp.status_code == 400


# ---------- CP07 / RF06: prioridad ----------
@pytest.mark.parametrize("prioridad", ["Alta", "Media", "Baja"])
def test_cp07_prioridad(client, prioridad):
    resp = crear(client, prioridad=prioridad)
    assert resp.get_json()["prioridad"] == prioridad


def test_prioridad_por_defecto_media(client):
    assert crear(client).get_json()["prioridad"] == "Media"


# ---------- Operación ----------
def test_pagina_principal_carga(client):
    resp = client.get("/")
    assert resp.status_code == 200
    assert b"TaskManager" in resp.data


def test_health(client):
    resp = client.get("/health")
    assert resp.status_code == 200
    assert resp.get_json() == {"status": "ok"}
