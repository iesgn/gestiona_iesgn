"""
Utilidades para el cierre de curso de la Dual: curso académico,
ficheros de historial (historial_<curso>.json) y generación de su contenido.
"""
import json
import re
from pathlib import Path

from django.conf import settings
from django.utils import timezone

from .models import AlumnoEmpresa, Curso

RE_CURSO = re.compile(r"(\d{4})-(\d{4})")
RE_FICHERO = re.compile(r"historial_(\d{4}-\d{4})\.json")


def curso_por_defecto():
    """Curso que acaba de terminar o está en marcha.

    Tanto en enero-agosto (curso en marcha) como en septiembre-diciembre
    (limpieza del curso anterior) es siempre «año anterior-año actual».
    """
    anio = timezone.localdate().year
    return f"{anio - 1}-{anio}"


def curso_valido(curso):
    m = RE_CURSO.fullmatch(curso or "")
    return bool(m) and int(m.group(2)) == int(m.group(1)) + 1


def directorio():
    return Path(settings.HISTORIAL_DUAL_DIR)


def ruta(curso):
    return directorio() / f"historial_{curso}.json"


def cursos_disponibles():
    """Cursos con fichero de historial, del más reciente al más antiguo."""
    if not directorio().is_dir():
        return []
    cursos = [m.group(1) for f in directorio().iterdir() if (m := RE_FICHERO.fullmatch(f.name))]
    return sorted(cursos, reverse=True)


def leer(curso):
    with open(ruta(curso), encoding="utf-8") as f:
        return json.load(f)


def generar(curso_academico):
    """Construye el informe curso -> empresa -> alumnos con los alumnos ASIGNADOS."""
    # Orden de los cursos según CODE_CHOICES (1SMR, 2SMR, 1ASIR, 2ASIR)
    orden = [code for code, _ in Curso.CODE_CHOICES]
    cursos = sorted(Curso.objects.all(), key=lambda c: orden.index(c.code) if c.code in orden else len(orden))
    bloques = {c.nombre: {"code": c.code, "nombre": c.nombre, "empresas": {}} for c in cursos}

    alumnos = (
        AlumnoEmpresa.objects.filter(estado=AlumnoEmpresa.Estado.ASIGNADO)
        .select_related("empresa")
    )
    for a in alumnos:
        bloque = bloques.setdefault(
            a.curso or "Sin curso",
            {"code": "", "nombre": a.curso or "Sin curso", "empresas": {}},
        )
        empresa = bloque["empresas"].setdefault(a.empresa_id, {
            "nombre": a.empresa.nombre.strip(),
            "localidad": a.empresa.localidad.strip(),
            "alumnos": [],
        })
        empresa["alumnos"].append({"uid": a.uid, "nombre": (a.nombre or a.uid).strip()})

    resultado = []
    for bloque in bloques.values():
        empresas = sorted(bloque["empresas"].values(), key=lambda e: e["nombre"].lower())
        for e in empresas:
            e["alumnos"].sort(key=lambda x: x["nombre"].lower())
        resultado.append({"code": bloque["code"], "nombre": bloque["nombre"], "empresas": empresas})

    return {
        "curso_academico": curso_academico,
        "generado": timezone.localtime().isoformat(timespec="seconds"),
        "cursos": resultado,
    }


def guardar(datos):
    directorio().mkdir(parents=True, exist_ok=True)
    destino = ruta(datos["curso_academico"])
    with open(destino, "w", encoding="utf-8") as f:
        json.dump(datos, f, ensure_ascii=False, indent=2)
    return destino
