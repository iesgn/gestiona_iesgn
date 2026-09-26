from django.core import serializers
from django.core.management.base import BaseCommand, CommandError
from django.db import transaction
from django.db.models import Count
from django.utils import timezone

from empresas import historial_dual
from empresas.models import AlumnoEmpresa, Empresa, HistorialAlumno
from empresas.management.commands.registrar_dual import prefijo


class Command(BaseCommand):
    help = (
        "Borra todas las asignaciones de alumnos a empresas (y su seguimiento) para "
        "empezar un curso nuevo. Antes comprueba que el curso está registrado en el "
        "historial (registrar_dual) y en el informe (informe_dual), y guarda una copia "
        "de lo borrado en HISTORIAL_DUAL_DIR."
    )

    def add_arguments(self, parser):
        parser.add_argument("--curso", default=historial_dual.curso_por_defecto(),
                            help="Curso académico que se cierra, p. ej. 2025-2026 (por defecto: %(default)s).")
        parser.add_argument("--dry-run", action="store_true",
                            help="Muestra lo que se borraría sin borrar nada.")
        parser.add_argument("--noinput", "--no-input", action="store_false", dest="interactive",
                            help="No pide confirmación.")
        parser.add_argument("--force", action="store_true",
                            help="Borra aunque falten el informe o entradas en el historial.")

    def handle(self, *args, curso, dry_run=False, interactive=True, force=False, **options):
        if not historial_dual.curso_valido(curso):
            raise CommandError(f"Curso no válido: {curso!r}. Formato esperado: 2025-2026.")

        alumnos = AlumnoEmpresa.objects.all()
        seguimiento = HistorialAlumno.objects.all()
        n_alumnos, n_seguimiento = alumnos.count(), seguimiento.count()

        self.stdout.write(f"Curso que se cierra: {curso}")
        if not n_alumnos:
            self.stdout.write(self.style.SUCCESS("No hay asignaciones de alumnos. Nada que hacer."))
            return

        for fila in alumnos.values("estado").annotate(n=Count("id")).order_by("estado"):
            etiqueta = AlumnoEmpresa.Estado(fila["estado"]).label if fila["estado"] else "Sin estado"
            self.stdout.write(f"  {etiqueta}: {fila['n']} alumnos")
        self.stdout.write(f"  Registros de seguimiento de alumnos: {n_seguimiento}")

        # === Comprobaciones previas ===
        problemas = []
        if not historial_dual.ruta(curso).exists():
            problemas.append(f"No existe el informe {historial_dual.ruta(curso)} (ejecuta informe_dual).")
        sin_historial = (
            Empresa.objects.filter(alumnos__estado=AlumnoEmpresa.Estado.ASIGNADO)
            .exclude(historial_contactos__texto__startswith=prefijo(curso))
            .distinct()
        )
        if sin_historial.exists():
            problemas.append(
                f"{sin_historial.count()} empresas con alumnos asignados no tienen la entrada "
                f"del curso {curso} en su historial (ejecuta registrar_dual)."
            )
        for p in problemas:
            self.stdout.write(self.style.ERROR(f"  ✗ {p}"))
        if problemas and not force:
            raise CommandError("Faltan pasos previos. Usa --force para borrar igualmente.")

        if dry_run:
            self.stdout.write(self.style.SUCCESS(
                f"\n[dry-run] Se borrarían {n_alumnos} asignaciones y {n_seguimiento} registros de seguimiento."
            ))
            return

        if interactive:
            respuesta = input(
                f"\nSe van a borrar {n_alumnos} asignaciones y {n_seguimiento} registros de seguimiento.\n"
                "Escribe 'si' para continuar: "
            )
            if respuesta.strip().lower() not in ("si", "sí"):
                raise CommandError("Operación cancelada.")

        # === Copia de seguridad de lo que se borra ===
        historial_dual.directorio().mkdir(parents=True, exist_ok=True)
        marca = timezone.localtime().strftime("%Y%m%d-%H%M%S")
        copia = historial_dual.directorio() / f"copia_alumnos_{curso}_{marca}.json"
        with open(copia, "w", encoding="utf-8") as f:
            serializers.serialize(
                "json", list(alumnos) + list(seguimiento), stream=f,
                indent=2, ensure_ascii=False,
            )
        self.stdout.write(f"Copia de seguridad: {copia}")

        with transaction.atomic():
            # El seguimiento se borra en cascada con cada AlumnoEmpresa
            total, detalle = alumnos.delete()

        self.stdout.write(self.style.SUCCESS(
            f"Borrado: {detalle.get('empresas.AlumnoEmpresa', 0)} asignaciones y "
            f"{detalle.get('empresas.HistorialAlumno', 0)} registros de seguimiento."
        ))
