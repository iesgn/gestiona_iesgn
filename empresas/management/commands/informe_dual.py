from django.core.management.base import BaseCommand, CommandError

from empresas import historial_dual


class Command(BaseCommand):
    help = (
        "Genera el informe estático historial_<curso>.json (curso -> empresa -> alumnos) "
        "con los alumnos asignados que hicieron la Dual en el curso indicado."
    )

    def add_arguments(self, parser):
        parser.add_argument("--curso", default=historial_dual.curso_por_defecto(),
                            help="Curso académico, p. ej. 2025-2026 (por defecto: %(default)s).")
        parser.add_argument("--dry-run", action="store_true",
                            help="Muestra el resumen sin escribir el fichero.")
        parser.add_argument("--force", action="store_true",
                            help="Sobrescribe el fichero si ya existe.")

    def handle(self, *args, curso, dry_run=False, force=False, **options):
        if not historial_dual.curso_valido(curso):
            raise CommandError(f"Curso no válido: {curso!r}. Formato esperado: 2025-2026.")

        destino = historial_dual.ruta(curso)
        if destino.exists() and not force and not dry_run:
            raise CommandError(f"{destino} ya existe. Usa --force para sobrescribirlo.")

        datos = historial_dual.generar(curso)

        self.stdout.write(f"Curso: {curso}")
        for bloque in datos["cursos"]:
            n_alumnos = sum(len(e["alumnos"]) for e in bloque["empresas"])
            self.stdout.write(
                f"  {bloque['nombre']}: {len(bloque['empresas'])} empresas, {n_alumnos} alumnos"
            )

        if dry_run:
            self.stdout.write(self.style.SUCCESS(f"\n[dry-run] Se escribiría {destino}"))
        else:
            historial_dual.guardar(datos)
            self.stdout.write(self.style.SUCCESS(f"\nInforme guardado en {destino}"))
