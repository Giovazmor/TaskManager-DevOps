# Historias de usuario

| ID | Historia | Criterios de aceptación |
|----|----------|-------------------------|
| HU1 | Como usuario del sistema, quiero registrar nuevas tareas para organizar mis actividades. | Ingresar nombre; agregar descripción; seleccionar prioridad; guardar la tarea; mostrar mensaje de confirmación. |
| HU2 | Como usuario, quiero ver todas las tareas registradas para conocer el trabajo pendiente. | Muestra el listado completo con nombre, descripción, prioridad y estado; mensaje si no hay tareas. |
| HU3 | Como usuario, quiero modificar una tarea para corregir o actualizar sus datos. | Carga la tarea en el formulario; permite cambiar nombre, descripción, prioridad y estado; el cambio se refleja en el listado. |
| HU4 | Como usuario, quiero eliminar tareas que ya no son necesarias. | Pide confirmación; la tarea desaparece del listado. |
| HU5 | Como usuario, quiero cambiar el estado de una tarea para conocer su progreso. | Permite pendiente, en proceso y terminada; el cambio se refleja en el listado. |
| HU6 | Como usuario, quiero clasificar las tareas como alta, media o baja. | Permite elegir la prioridad; se guarda y se muestra con indicador visual; por defecto es media. |
| HU7 | Como usuario, quiero que el sistema valide los datos para evitar registros incorrectos. | No guarda tareas sin nombre; rechaza estados y prioridades inválidos; muestra un mensaje claro. |
| HU8 | Como empresa, quiero pruebas automáticas antes de integrar cambios. | Cada push y Pull Request a `main` ejecuta las pruebas; si fallan, se corrigen antes de integrar. |
