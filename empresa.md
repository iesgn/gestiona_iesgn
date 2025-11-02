# Módulo de Empresas

Objetivo: Gestionar la base de datos de empresas, historial de contactos, alumnos asignados y seguimiento de los alumnos.

## Nueva empresa

Damos de alta a las empresas. 

* El único campo requerido es el **Nombre**.
* 3 estados: 
    * Colabora: Ya se ha confirmado que coge a algún alumno. (VERDE)
    * En contacto: Estamos en el proceso de ponernos de acuerdo. (AMARILLO)
    * No colabora: Este curso no colabora, pero la tenemos guardada. (ROJO)
* Plazas ofrecidas por curso:
    * Nos permite indicar con que curso trabaja la empresa (poniendo alguna plaza a ese curso).
    * Cuando sepamos las plazas no s permite ajustar el número de plazas para saber los alumnos que tenemos que asignar.

## Operaciones sobre las empresas:

### Editar y borrar

### Historial de contacto

Durante la etapa de contacto con la empresa nos permite dejar registro de los contactos que se tiene con la empresa. Podemos guardar diferentes informaciones:

* Estado del proceso (he llamado, he enviado un correo, esperando respuesta...).
* Indicaciones de la empresa (mandar 3 CV).
* Datos para realizar el acuerdo.

De cada evento, se guarda la fecha y hora, el profesor que lo ha realizado y la información.
Se ordena de más nuevo a más antiguo.

### Alumnos asignados

Según los cursos con los que trabaje la empresa nos mostrará los alumnos del curso.
* Si el alumno va a esa empresa, escogemos el check inicial.
* El alumno tiene 3 estados:
    * Ninguno: El alumno se asigna a la empresa como propuesta.
    * En proceso: El alumno está en un proceso selectivo o todavía no está claro de que lo vayan a escoger.
    * Asignado: El alumno hace la fase dual en esa empresa.

En la página principal, aparecen los alumnos indicando el estado. Si está asignado el nombre del alumno será un enlace que nos permite entrar en la página de seguimiento del alumno.

### Personas de contacto

Nos permite guardar las personas de contactos de las empresas indicando nombre, correo y teléfono.

## Seguimiento del alumnado

Como hemos comentado un alumno con estado **Seleccionado** aparecerá en la página principal con un enlace en el nombre que permite acceder a la página se **Seguimiento del alumno**
* El seguimiento del alumno funciona de forma similar al historial de contactos de las empresas: es decir, el profesor deja un comentario sobre el proceso de seguimiento del alumno.
* en la lista de alumnos de la empresa, aparecerá un aviso de que el alumnos tiene seguimiento, ya que si lo desmarcamos, ese alumno ya no estará relacionado con la empresa y se borrará los comentarios del seguimiento.

## Otras funcionalidades

* Filtro en la página principal: Podemos buscar por empresa, por alumno, por localidad o por CIF. Además podemos seleccionar por estado de la empresa y por cursos.
* Resumen de plazas asignadas / plazas solicitadas.


