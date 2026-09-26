# gestiona_iesgn
Programa desarrollado en django para gestionar usuarios del LDAP del departamento de informática del IES Gonzalo Nazareno


## App Empresas: cambio de curso

Al empezar un curso nuevo hay que dejar constancia de los alumnos que hicieron la Dual en el curso anterior y después vaciar las asignaciones de alumnos a empresas. Se hace con tres comandos de gestión, **en este orden**:

| Paso | Comando | Qué hace |
|---|---|---|
| 1 | `registrar_dual` | Añade al historial de contactos de cada empresa una entrada con sus alumnos asignados: *"En el curso 2025-2026 los alumnos que hicieron la Dual en esta empresa son: …"* |
| 2 | `informe_dual` | Genera el informe estático `historial_dual/historial_<curso>.json` (curso → empresa → alumnos), que se consulta desde el botón **Historial por años** de la lista de empresas. |
| 3 | `limpiar_dual` | Borra todas las asignaciones de alumnos a empresas y su seguimiento. |

Solo se tienen en cuenta los alumnos con estado **Asignado**.

### Procedimiento

Antes de empezar, haz una copia de la base de datos.

```bash
# 1. Historial de cada empresa
python manage.py registrar_dual --dry-run
python manage.py registrar_dual

# 2. Informe estático
python manage.py informe_dual --dry-run
python manage.py informe_dual

# 3. Limpieza de asignaciones (pide escribir "si" para confirmar)
python manage.py limpiar_dual --dry-run
python manage.py limpiar_dual
```

En producción, añade `--settings=gestiona_iesgn.settings.prod` a cada comando o define `DJANGO_SETTINGS_MODULE`.

### Opciones

Las tres órdenes admiten:

- `--curso AAAA-AAAA`: curso que se cierra. Por defecto es «año anterior-año actual» (en septiembre de 2026, `2025-2026`).
- `--dry-run`: muestra lo que haría sin modificar nada.

Además:

- `informe_dual --force`: sobrescribe el informe si ya existe. Sin esta opción el comando se niega.
- `limpiar_dual --noinput`: no pide confirmación.
- `limpiar_dual --force`: borra aunque falten los pasos 1 o 2.

### Seguridad

- `registrar_dual` se puede ejecutar varias veces: salta las empresas que ya tienen la entrada de ese curso.
- `limpiar_dual` no borra nada si falta el informe del curso o si alguna empresa con alumnos asignados no tiene su entrada en el historial.
- Antes de borrar, `limpiar_dual` guarda una copia de lo eliminado en `historial_dual/copia_alumnos_<curso>_<fecha>.json`. Se restaura con:

  ```bash
  python manage.py loaddata historial_dual/copia_alumnos_<curso>_<fecha>.json
  ```

### Directorio `historial_dual/`

- Su ubicación se configura con `HISTORIAL_DUAL_DIR` en `gestiona_iesgn/settings/base.py` (por defecto, `historial_dual/` en la raíz del proyecto).
- Contiene datos personales de alumnos, así que está en `.gitignore` y no se sirve como fichero estático: solo se ve desde la aplicación con sesión de profesor.
- Debe conservarse entre despliegues e incluirse en las copias de seguridad del servidor.
