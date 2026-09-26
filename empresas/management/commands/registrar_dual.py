from django.core.management.base import BaseCommand, CommandError
from django.db import transaction

from empresas import historial_dual
from empresas.models import Empresa, AlumnoEmpresa, HistorialContacto


def prefijo(curso):
    return f"En el curso {curso}"


def texto_alumnos(curso, alumnos):
    if len(alumnos) == 1:
        cabecera = f"{prefijo(curso)} el alumno que hizo la Dual en esta empresa es:"
    else:
        cabecera = f"{prefijo(curso)} los alumnos que hicieron la Dual en esta empresa son:"
    lineas = [f"- {(a.nombre or a.uid).strip()} ({a.curso})" for a in alumnos]
    return "\n".join([cabecera] + lineas)


class Command(BaseCommand):
    help = (
        "Añade al historial de cada empresa una entrada con los alumnos asignados "
        "que hicieron la Dual en el curso indicado."
    )

    def add_arguments(self, parser):
        parser.add_argument("--curso", default=historial_dual.curso_por_defecto(),
                            help="Curso académico, p. ej. 2025-2026 (por defecto: %(default)s).")
        parser.add_argument("--dry-run", action="store_true",
                            help="Muestra lo que se haría sin guardar nada.")

    @transaction.atomic
    def handle(self, *args, curso, dry_run=False, **options):
        if not historial_dual.curso_valido(curso):
            raise CommandError(f"Curso no válido: {curso!r}. Formato esperado: 2025-2026.")
        self.stdout.write(f"Curso: {curso}")

        creadas = omitidas = 0
        empresas = Empresa.objects.filter(
            alumnos__estado=AlumnoEmpresa.Estado.ASIGNADO
        ).distinct().order_by("nombre")

        for empresa in empresas:
            if empresa.historial_contactos.filter(texto__startswith=prefijo(curso)).exists():
                self.stdout.write(self.style.WARNING(f"[ya existe] {empresa.nombre}"))
                omitidas += 1
                continue

            alumnos = list(
                empresa.alumnos.filter(estado=AlumnoEmpresa.Estado.ASIGNADO)
                .order_by("curso", "nombre")
            )
            texto = texto_alumnos(curso, alumnos)
            self.stdout.write(f"\n== {empresa.nombre}\n{texto}")

            if not dry_run:
                HistorialContacto.objects.create(
                    empresa=empresa,
                    profesor_username="sistema",
                    profesor_nombre="Registro automático",
                    texto=texto,
                )
            creadas += 1

        accion = "se crearían" if dry_run else "creadas"
        self.stdout.write(self.style.SUCCESS(
            f"\nEntradas {accion}: {creadas}. Empresas omitidas (ya registradas): {omitidas}."
        ))
