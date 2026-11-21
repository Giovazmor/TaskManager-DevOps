const $ = (id) => document.getElementById(id);
const form = $("form-tarea");

function mostrarMensaje(texto, tipo) {
  const el = $("mensaje");
  el.textContent = texto;
  el.className = tipo || "";
}

function esc(texto) {
  const d = document.createElement("div");
  d.textContent = texto ?? "";
  return d.innerHTML;
}

async function api(url, opciones = {}) {
  const resp = await fetch(url, {
    headers: { "Content-Type": "application/json" },
    ...opciones,
  });
  if (resp.status === 204) return null;
  const datos = await resp.json();
  if (!resp.ok) throw new Error(datos.error || "Error inesperado");
  return datos;
}

async function cargar() {
  const tareas = await api("/api/tareas");
  $("contador").textContent = `(${tareas.length})`;
  const lista = $("lista");
  if (!tareas.length) {
    lista.innerHTML = '<p class="vacio">No hay tareas registradas.</p>';
    return;
  }
  lista.innerHTML = tareas
    .map(
      (t) => `
    <article class="tarea ${t.prioridad} ${t.estado === "Terminada" ? "Terminada" : ""}">
      <h3>${esc(t.nombre)}</h3>
      <p>${esc(t.descripcion) || "<em>Sin descripción</em>"}</p>
      <div class="acciones">
        <span class="etiqueta">Prioridad: ${esc(t.prioridad)}</span>
        <select data-estado="${t.id}" aria-label="Estado">
          ${["Pendiente", "En proceso", "Terminada"]
            .map((e) => `<option ${e === t.estado ? "selected" : ""}>${e}</option>`)
            .join("")}
        </select>
        <button class="chico" data-editar="${t.id}">Editar</button>
        <button class="chico peligro" data-eliminar="${t.id}">Eliminar</button>
      </div>
    </article>`
    )
    .join("");
}

function reiniciarFormulario() {
  form.reset();
  $("tarea-id").value = "";
  $("form-titulo").textContent = "Nueva tarea";
  $("btn-guardar").textContent = "Guardar tarea";
  $("btn-cancelar").hidden = true;
}

form.addEventListener("submit", async (ev) => {
  ev.preventDefault();
  const id = $("tarea-id").value;
  const cuerpo = {
    nombre: $("nombre").value,
    descripcion: $("descripcion").value,
    prioridad: $("prioridad").value,
    estado: $("estado").value,
  };
  try {
    if (id) {
      await api(`/api/tareas/${id}`, { method: "PUT", body: JSON.stringify(cuerpo) });
      mostrarMensaje("Tarea actualizada correctamente.", "ok");
    } else {
      await api("/api/tareas", { method: "POST", body: JSON.stringify(cuerpo) });
      mostrarMensaje("Tarea guardada correctamente.", "ok");
    }
    reiniciarFormulario();
    await cargar();
  } catch (e) {
    mostrarMensaje(e.message, "error");
  }
});

$("btn-cancelar").addEventListener("click", () => {
  reiniciarFormulario();
  mostrarMensaje("");
});

$("lista").addEventListener("click", async (ev) => {
  const idEditar = ev.target.dataset.editar;
  const idEliminar = ev.target.dataset.eliminar;
  try {
    if (idEditar) {
      const tareas = await api("/api/tareas");
      const t = tareas.find((x) => String(x.id) === idEditar);
      $("tarea-id").value = t.id;
      $("nombre").value = t.nombre;
      $("descripcion").value = t.descripcion;
      $("prioridad").value = t.prioridad;
      $("estado").value = t.estado;
      $("form-titulo").textContent = "Editar tarea";
      $("btn-guardar").textContent = "Actualizar tarea";
      $("btn-cancelar").hidden = false;
      window.scrollTo({ top: 0, behavior: "smooth" });
    } else if (idEliminar && confirm("¿Eliminar esta tarea?")) {
      await api(`/api/tareas/${idEliminar}`, { method: "DELETE" });
      mostrarMensaje("Tarea eliminada.", "ok");
      await cargar();
    }
  } catch (e) {
    mostrarMensaje(e.message, "error");
  }
});

$("lista").addEventListener("change", async (ev) => {
  const id = ev.target.dataset.estado;
  if (!id) return;
  try {
    await api(`/api/tareas/${id}/estado`, {
      method: "PATCH",
      body: JSON.stringify({ estado: ev.target.value }),
    });
    mostrarMensaje("Estado actualizado.", "ok");
    await cargar();
  } catch (e) {
    mostrarMensaje(e.message, "error");
  }
});

cargar().catch((e) => mostrarMensaje(e.message, "error"));
