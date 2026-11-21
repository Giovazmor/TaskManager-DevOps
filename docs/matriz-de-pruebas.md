# Matriz de casos de prueba

| ID | Prueba | Resultado esperado | Prueba automatizada | Resultado |
|----|--------|--------------------|---------------------|-----------|
| CP01 | Registrar una tarea | La tarea se guarda correctamente. | `test_cp01_registrar_tarea` | Aprobada |
| CP02 | Registrar una tarea sin nombre | El sistema muestra una validación. | `test_cp02_registrar_sin_nombre` | Aprobada |
| CP03 | Consultar tareas | Se muestra el listado. | `test_cp03_consultar_tareas` | Aprobada |
| CP04 | Editar una tarea | Se actualiza la información. | `test_cp04_editar_tarea` | Aprobada |
| CP05 | Eliminar una tarea | La tarea desaparece del listado. | `test_cp05_eliminar_tarea` | Aprobada |
| CP06 | Cambiar estado | Se actualiza el estado. | `test_cp06_cambiar_estado` | Aprobada |
| CP07 | Seleccionar prioridad | Se guarda la prioridad elegida. | `test_cp07_prioridad` | Aprobada |

Ejecutar con `pytest -v`. Las pruebas funcionales manuales se registran con capturas de pantalla.
