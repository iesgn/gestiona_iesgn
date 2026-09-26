from django.shortcuts import render, get_object_or_404, redirect
from django.db.models import Count, Q, Sum
from django.views.decorators.http import require_POST
from gestiona_iesgn.views import profesor_required
from .forms import EmpresaForm
from .models import Empresa, PersonaContacto, AlumnoEmpresa, HistorialContacto,Curso, PlazaCurso,HistorialAlumno
from usuarios.libldap import LibLDAP
from django.utils import timezone
from django.contrib import messages
from django.conf import settings
from django.http import Http404
from . import historial_dual


# Clave de sesión donde se recuerdan los filtros de la lista de empresas
FILTROS_SESION = "empresas_filtros"
PARAMETROS_FILTRO = ("q", "estado", "curso", "profesor", "libres")

# Curso.code -> grupo LDAP
CURSO_TO_LDAP_GROUP = {
    "1SMR": "smr1",
    "2SMR": "smr2",
    "1ASIR": "asir1",
    "2ASIR": "asir2",
}


def _alumnos_de_grupo(ldap, grupo):
    """
    Alumnos de un grupo LDAP (uid, nombre, email), ordenados por nombre.
    Usa el atributo memberOf de los usuarios, igual que la app grupos:
    la lista `member` del grupo puede tener restos de usuarios que ya no existen.
    """
    alumnos = []
    for e in ldap.buscar(ldap.conv_filtro({"grupo": grupo}), ["uid", "cn", "mail"]):
        uid = e.get("uid", [""])[0]
        alumnos.append({
            "uid": uid,
            "nombre": (e.get("cn") or [uid])[0],
            "email": (e.get("mail") or [""])[0],
        })
    return sorted(alumnos, key=lambda a: a["nombre"].lower())


def _url_lista():
    """URL de la lista de empresas; los filtros se recuperan de la sesión."""
    return settings.SITE_URL + "/empresas/"


def _profesor_actual(request):
    """Devuelve (username, nombre) del profesor logueado, con el nombre desde LDAP."""
    username = request.session.get("username", "desconocido")
    nombre = username
    try:
        entradas = LibLDAP().buscar(f"(uid={username})", ["cn"])
        if entradas:
            nombre = entradas[0].get("cn", [username])[0]
    except Exception:
        pass
    return username, nombre


def _fecha_formulario(fecha_str):
    """Convierte el valor de un input datetime-local a fecha con zona horaria."""
    try:
        fecha = timezone.datetime.fromisoformat(fecha_str)
    except (TypeError, ValueError):
        return timezone.now()
    if timezone.is_naive(fecha):
        fecha = timezone.make_aware(fecha)
    return fecha


ESTADOS_EMPRESA = [
    ("verde", "Colabora"),
    ("naranja", "En contacto"),
    ("rojo", "No colabora"),
]


def _leer_filtros(params):
    """Extrae los filtros de la lista de empresas de un QueryDict."""
    return {
        "q": (params.get("q") or "").strip(),
        "estados": params.getlist("estado"),
        "cursos": params.getlist("curso"),
        "profesor": (params.get("profesor") or "").strip(),
        "libres": params.get("libres") == "1",
    }


def _describir_filtros(f):
    """Descripción legible de los filtros aplicados."""
    filtros = []
    if f["q"]:
        filtros.append(f"Búsqueda: «{f['q']}»")
    if f["estados"]:
        nombres = dict(ESTADOS_EMPRESA)
        filtros.append("Estado: " + ", ".join(nombres.get(e, e) for e in f["estados"]))
    if f["cursos"]:
        nombres = dict(Curso.objects.values_list("code", "nombre"))
        filtros.append("Cursos: " + ", ".join(nombres.get(c, c) for c in f["cursos"]))
    if f["profesor"]:
        filtros.append(f"Profesor: {f['profesor']}")
    if f["libres"]:
        filtros.append("Con plazas libres")
    return filtros


def _profesores_responsables():
    """Valores distintos de profesor_responsable, para el desplegable del filtro."""
    valores = (
        Empresa.objects.exclude(profesor_responsable="")
        .values_list("profesor_responsable", flat=True).distinct()
    )
    return sorted({v.strip() for v in valores if v.strip()}, key=str.lower)


def _empresas_filtradas(f):
    """
    Devuelve la lista de empresas que cumplen los filtros (ver _leer_filtros),
    ordenada por estado y nombre, con `plazas_info` calculado.
    """
    empresas = Empresa.objects.prefetch_related("plazas_curso__curso", "alumnos", "contactos")

    q = f["q"]
    if q:
        empresas = empresas.filter(
            Q(nombre__icontains=q)
            | Q(localidad__icontains=q)
            | Q(cif__icontains=q)
            | Q(profesor_responsable__icontains=q)
            | Q(alumnos__nombre__icontains=q)
            | Q(alumnos__uid__icontains=q)
        ).distinct()

    if f["estados"]:
        empresas = empresas.filter(estado__in=f["estados"])

    if f["cursos"]:
        # Filtramos por cursos ofertados con plazas > 0
        empresas = empresas.filter(
            plazas_curso__curso__code__in=f["cursos"],
            plazas_curso__plazas__gt=0
        ).distinct()

    if f["profesor"]:
        # icontains: "Conchi" incluye también "Conchi Guisado"
        empresas = empresas.filter(profesor_responsable__icontains=f["profesor"])

    # Orden personalizado por estado + nombre
    estado_order = {"verde": 0, "naranja": 1, "rojo": 2}
    empresas = sorted(
        empresas,
        key=lambda e: (estado_order.get(e.estado, 99), e.nombre.lower())
    )

    # Información de plazas y alumnos por empresa
    for e in empresas:
        e.plazas_info = []
        for p in e.plazas_curso.all():
            if p.plazas > 0:
                num_alumnos = sum(1 for a in e.alumnos.all() if a.curso == p.curso.nombre)
                e.plazas_info.append({
                    "curso_code": p.curso.code,
                    "curso_nombre": p.curso.nombre,
                    "plazas": p.plazas,
                    "ocupadas": num_alumnos,
                })

    if f["libres"]:
        # Empresas con alguna plaza libre (en los cursos filtrados, si los hay)
        empresas = [
            e for e in empresas
            if any(
                i["ocupadas"] < i["plazas"]
                for i in e.plazas_info
                if not f["cursos"] or i["curso_code"] in f["cursos"]
            )
        ]
    return empresas


def _alumnos_repetidos():
    """Alumnos asignados a más de una empresa: lista de (nombre, [empresas])."""
    uids = (
        AlumnoEmpresa.objects.values("uid").annotate(n=Count("empresa", distinct=True))
        .filter(n__gt=1).values_list("uid", flat=True)
    )
    repetidos = {}
    for a in AlumnoEmpresa.objects.filter(uid__in=list(uids)).select_related("empresa").order_by("nombre"):
        dato = repetidos.setdefault(a.uid, {"nombre": (a.nombre or a.uid).strip(), "empresas": []})
        dato["empresas"].append(a.empresa.nombre)
    return list(repetidos.values())


@profesor_required
def lista_empresas(request):
    """
    Muestra el listado de empresas con filtros por búsqueda, estado, cursos,
    profesor y plazas libres. Además calcula un resumen global de plazas y
    alumnos por curso.
    """

    # === 0. Recordar / recuperar / limpiar filtros en la sesión ===
    if "limpiar" in request.GET:
        request.session.pop(FILTROS_SESION, None)
        return redirect(_url_lista())
    if any(p in request.GET for p in PARAMETROS_FILTRO):
        request.session[FILTROS_SESION] = request.GET.urlencode()
    elif request.session.get(FILTROS_SESION):
        return redirect(_url_lista() + "?" + request.session[FILTROS_SESION])

    # === 1-5. Empresas filtradas con su información de plazas ===
    f = _leer_filtros(request.GET)
    cursos = f["cursos"]
    empresas = _empresas_filtradas(f)

    # === 6. Resumen global de plazas y alumnos por curso ===
    empresa_ids = [e.id for e in empresas]  # usar IDs evita duplicados

    resumen_cursos = []
    cursos_para_resumen = (
        Curso.objects.filter(code__in=cursos) if cursos else Curso.objects.all()
    )

    for curso in cursos_para_resumen:
        plazas_totales = PlazaCurso.objects.filter(
            empresa_id__in=empresa_ids, curso=curso
        ).aggregate(total=Sum("plazas"))["total"] or 0

        alumnos_totales = AlumnoEmpresa.objects.filter(
            empresa_id__in=empresa_ids, curso=curso.nombre
        ).count()

        resumen_cursos.append({
            "nombre": curso.nombre,
            "plazas": plazas_totales,
            "alumnos": alumnos_totales,
        })
    # === 7. Renderizado ===
    context = {
        "object_list": empresas,
        "cursos": Curso.objects.all(),
        "estados": ESTADOS_EMPRESA,
        "estados_seleccionados": f["estados"],
        "cursos_seleccionados": cursos,
        "busqueda": f["q"],
        "profesores": _profesores_responsables(),
        "profesor_seleccionado": f["profesor"],
        "libres": f["libres"],
        "hay_filtros": bool(_describir_filtros(f)),
        "resumen_cursos": resumen_cursos,
        "alumnos_repetidos": _alumnos_repetidos(),
        "hay_historial_dual": bool(historial_dual.cursos_disponibles()),
    }

    return render(request, "empresas/lista.html", context)


@profesor_required
def nueva_empresa(request):
    if request.method == "POST":
        form = EmpresaForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect(_url_lista())
    else:
        form = EmpresaForm()
    return render(request, "empresas/form.html", {"form": form})


@profesor_required
def editar_empresa(request, pk):
    empresa = get_object_or_404(Empresa, pk=pk)
    if request.method == "POST":
        form = EmpresaForm(request.POST, instance=empresa)
        if form.is_valid():
            form.save()
            return redirect(_url_lista())
    else:
        form = EmpresaForm(instance=empresa)
    return render(request, "empresas/form.html", {"form": form})

@profesor_required
def borrar_empresa(request, pk):
    empresa = get_object_or_404(Empresa, pk=pk)

    if request.method == "POST":
        empresa.delete()
        return redirect(_url_lista())

    return render(request, "empresas/confirm_delete.html", {"object": empresa})


@profesor_required
def historial_empresa(request, pk):
    """
    Muestra y gestiona el historial de contactos de una empresa.
    - Añadir registros con fecha, hora y descripción.
    - Guardar el profesor logueado desde LDAP.
    - Permitir borrar entradas individuales.
    """
    empresa = get_object_or_404(Empresa, pk=pk)

    # === Procesamiento POST (añadir o borrar) ===
    if request.method == "POST":
        if "borrar" in request.POST:
            # Borrar registro concreto
            contacto_id = request.POST.get("borrar")
            HistorialContacto.objects.filter(pk=contacto_id, empresa=empresa).delete()
        else:
            # Crear nuevo registro
            texto = request.POST.get("texto", "").strip()
            if texto:
                profesor_username, profesor_nombre = _profesor_actual(request)
                HistorialContacto.objects.create(
                    empresa=empresa,
                    profesor_username=profesor_username,
                    profesor_nombre=profesor_nombre,
                    fecha=_fecha_formulario(request.POST.get("fecha")),
                    texto=texto
                )

        return redirect(settings.SITE_URL+"/empresas/"+str(pk)+"/historial/")

    # === En GET: mostrar historial ===
    historial = HistorialContacto.objects.filter(empresa=empresa).order_by('-fecha')

    return render(request, "empresas/historial.html", {
        "empresa": empresa,
        "historial": historial,
        "ahora": timezone.localtime(timezone.now()).strftime("%Y-%m-%dT%H:%M"),
    })

# === Alumnos ===
@profesor_required
def gestionar_alumnos(request, pk):
    empresa = get_object_or_404(Empresa, pk=pk)
    ldap = LibLDAP()

    # === 1. Cursos ofertados y alumnos actuales ===
    cursos_qs = Curso.objects.filter(
        plazacurso__empresa=empresa,
        plazacurso__plazas__gt=0
    ).distinct()

    alumnos = AlumnoEmpresa.objects.filter(empresa=empresa)
    existentes = [a.uid for a in alumnos]

    # === 2. Buscar alumnos en LDAP según cursos ofertados ===
    disponibles = []
    vistos = set()

    uids_con_seguimiento = set(
        HistorialAlumno.objects.filter(
            alumno__empresa=empresa
        ).values_list("alumno__uid", flat=True)
    )
    uids_con_seguimiento = {str(u).lower() for u in uids_con_seguimiento if u}

    for curso in cursos_qs:
        grupo = CURSO_TO_LDAP_GROUP.get(curso.code)
        if not grupo:
            continue

        for e in _alumnos_de_grupo(ldap, grupo):
            uid = e["uid"]
            if uid in vistos:
                continue
            vistos.add(uid)

            seguimiento_activo = uid.lower() in uids_con_seguimiento
            empresa_asignada = AlumnoEmpresa.objects.filter(uid=uid).exclude(empresa=empresa).first()
            nombre_empresa = empresa_asignada.empresa.nombre if empresa_asignada else ""

            alumno_existente = alumnos.filter(uid=uid).first()

            disponibles.append({
                "uid": uid,
                "nombre": e["nombre"],
                "email": e["email"],
                "curso": curso.nombre,
                "seleccionado": uid in existentes,
                "estado": alumno_existente.estado if alumno_existente else None,
                "fuera_de_curso": False,
                "empresa_asignada": nombre_empresa,
                "tiene_seguimiento": seguimiento_activo,
            })

    # === 3. Añadir alumnos guardados que ya no están en LDAP ===
    uids_ldap = {a["uid"] for a in disponibles}
    for guardado in alumnos:
        if guardado.uid not in uids_ldap:
            disponibles.append({
                "uid": guardado.uid,
                "nombre": guardado.nombre or guardado.uid,
                "email": "",
                "curso": guardado.curso or "—",
                "seleccionado": True,
                "estado": guardado.estado,
                "fuera_de_curso": True,
                "empresa_asignada": "",
                "tiene_seguimiento": guardado.uid.lower() in uids_con_seguimiento,
            })

    # === 4. Procesar guardado ===
    if request.method == "POST":
        seleccionados = request.POST.getlist("alumnos")

        # --- Eliminar alumnos desmarcados ---
        to_delete = AlumnoEmpresa.objects.filter(empresa=empresa).exclude(uid__in=seleccionados)
        for a in to_delete:
            if hasattr(a, "historial_alumno") and a.historial_alumno.exists():
                messages.warning(
                    request,
                    f"El alumno {a.nombre or a.uid} tenía historial de seguimiento que ha sido eliminado."
                )
        to_delete.delete()

        # --- Crear o actualizar seleccionados ---
        for a in disponibles:
            if a["uid"] in seleccionados and a["uid"]:
                estado_valor = request.POST.get(f"estado_{a['uid']}", "").strip() or None

                AlumnoEmpresa.objects.update_or_create(
                    empresa=empresa,
                    uid=a["uid"],
                    defaults={
                        "nombre": a["nombre"],
                        "curso": a["curso"],
                        "estado": estado_valor,
                    }
                )

        # --- Avisar de alumnos que también están en otras empresas ---
        otras = (
            AlumnoEmpresa.objects.filter(uid__in=seleccionados)
            .exclude(empresa=empresa).select_related("empresa")
        )
        for otra in otras:
            messages.warning(
                request,
                f"{otra.nombre or otra.uid} está asignado también a {otra.empresa.nombre}."
            )

        return redirect(_url_lista())


    # === 5. Renderizar plantilla ===
    return render(request, "empresas/alumnos.html", {
        "empresa": empresa,
        "disponibles": disponibles,
    })

# === Contactos ===
def _datos_contacto(request):
    return {
        "nombre": request.POST.get("nombre", "").strip(),
        "telefono": request.POST.get("telefono", "").strip(),
        "email": request.POST.get("email", "").strip(),
    }


def _url_contactos(empresa_id):
    return settings.SITE_URL + "/empresas/" + str(empresa_id) + "/contactos/"


@profesor_required
def gestionar_contactos(request, pk, editando=None):
    empresa = get_object_or_404(Empresa, pk=pk)

    if request.method == "POST":
        # Alta de un nuevo contacto
        datos = _datos_contacto(request)
        if datos["nombre"]:
            PersonaContacto.objects.create(empresa=empresa, **datos)
        return redirect(_url_contactos(pk))

    contactos = PersonaContacto.objects.filter(empresa=empresa)
    return render(request, "empresas/contactos.html", {
        "empresa": empresa,
        "contactos": contactos,
        "editando": editando,
    })


@profesor_required
def editar_contacto(request, contacto_id):
    contacto = get_object_or_404(PersonaContacto, pk=contacto_id)

    if request.method == "POST":
        datos = _datos_contacto(request)
        if datos["nombre"]:
            for campo, valor in datos.items():
                setattr(contacto, campo, valor)
            contacto.save()
        return redirect(_url_contactos(contacto.empresa_id))

    # En GET: la misma página de contactos con el formulario relleno
    return gestionar_contactos(request, contacto.empresa_id, editando=contacto)

@require_POST
@profesor_required
def borrar_contacto(request, contacto_id):
    contacto = get_object_or_404(PersonaContacto, pk=contacto_id)
    empresa_id = contacto.empresa_id
    contacto.delete()
    return redirect(_url_contactos(empresa_id))

# ==seguimiento

@profesor_required
def historial_alumno(request, alumno_id):
    """
    Muestra y gestiona el historial de seguimiento de un alumno.
    - Añadir registros con fecha, hora y observación.
    - Guardar el profesor logueado desde LDAP.
    - Permitir borrar entradas individuales.
    """
    alumno = get_object_or_404(AlumnoEmpresa, pk=alumno_id)
    empresa = alumno.empresa

    # === Procesamiento POST (añadir o borrar) ===
    if request.method == "POST":
        if "borrar" in request.POST:
            # Borrar registro concreto
            registro_id = request.POST.get("borrar")
            HistorialAlumno.objects.filter(pk=registro_id, alumno=alumno).delete()
        else:
            # Crear nuevo registro
            texto = request.POST.get("texto", "").strip()
            if texto:
                profesor_username, profesor_nombre = _profesor_actual(request)
                HistorialAlumno.objects.create(
                    alumno=alumno,
                    profesor_username=profesor_username,
                    profesor_nombre=profesor_nombre,
                    fecha=_fecha_formulario(request.POST.get("fecha")),
                    texto=texto,
                )

        return redirect(settings.SITE_URL+"/empresas/alumno/"+str(alumno.id)+"/historial/")

    # === En GET: mostrar historial ===
    historial = HistorialAlumno.objects.filter(alumno=alumno).order_by("-fecha")

    return render(request, "empresas/historial_alumno.html", {
        "empresa": empresa,
        "alumno": alumno,
        "historial": historial,
        "ahora": timezone.localtime(timezone.now()).strftime("%Y-%m-%dT%H:%M"),
    })


@profesor_required
def historial_dual_view(request):
    """
    Muestra el informe estático de cierre de curso de la Dual
    (curso -> empresa -> alumnos) leído de historial_<curso>.json.
    """
    disponibles = historial_dual.cursos_disponibles()
    if not disponibles:
        raise Http404("No hay informes de historial de la Dual.")

    curso = request.GET.get("curso") or disponibles[0]
    if curso not in disponibles:
        raise Http404(f"No existe el historial del curso {curso}.")

    datos = historial_dual.leer(curso)
    for bloque in datos["cursos"]:
        bloque["total_alumnos"] = sum(len(e["alumnos"]) for e in bloque["empresas"])

    return render(request, "empresas/historial_dual.html", {
        "disponibles": disponibles,
        "curso": curso,
        "datos": datos,
        "total_alumnos": sum(b["total_alumnos"] for b in datos["cursos"]),
    })


@profesor_required
def listado_empresas(request):
    """
    Informe imprimible con la información completa de las empresas que
    cumplen los filtros actuales de la lista.
    """
    f = _leer_filtros(request.GET)
    empresas = _empresas_filtradas(f)
    filtros = _describir_filtros(f)

    return render(request, "empresas/listado.html", {
        "empresas": empresas,
        "filtros": filtros,
        "ahora": timezone.localtime(),
    })


@profesor_required
def alumnos_sin_empresa(request):
    """
    Alumnos de los grupos LDAP de cada curso que no están asignados
    a ninguna empresa (en ningún estado).
    """
    ldap = LibLDAP()
    asignados = set(AlumnoEmpresa.objects.values_list("uid", flat=True))
    orden = [code for code, _ in Curso.CODE_CHOICES]
    cursos = sorted(Curso.objects.all(), key=lambda c: orden.index(c.code) if c.code in orden else len(orden))

    bloques = []
    for curso in cursos:
        grupo = CURSO_TO_LDAP_GROUP.get(curso.code)
        if not grupo:
            continue
        del_grupo = _alumnos_de_grupo(ldap, grupo)
        alumnos = [a for a in del_grupo if a["uid"] not in asignados]
        bloques.append({
            "curso": curso,
            "total": len(del_grupo),
            "asignados": len(del_grupo) - len(alumnos),
            "alumnos": alumnos,
        })

    return render(request, "empresas/sin_empresa.html", {
        "bloques": bloques,
        "total_sin_empresa": sum(len(b["alumnos"]) for b in bloques),
    })
