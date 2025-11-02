from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy
from django.db.models import Q
from gestiona_iesgn.views import test_profesor
from .forms import EmpresaForm
from .models import Empresa, PersonaContacto, AlumnoEmpresa, HistorialContacto,Curso, PlazaCurso,HistorialAlumno
from .services import alumnos_de_empresa
from usuarios.libldap import LibLDAP
from django.utils import timezone
from django.db import models
from django.db.models import Q, Sum
from django.contrib import messages



@csrf_exempt
def lista_empresas(request):
    """
    Muestra el listado de empresas con filtros por búsqueda, estado y cursos.
    Además calcula un resumen global de plazas y alumnos por curso.
    """
    test_profesor(request)

    # === 1. Obtener filtros de la petición ===
    q = request.GET.get("q")
    estados = request.GET.getlist("estado")
    cursos = request.GET.getlist("curso")

    # === 2. Construir queryset base ===
    empresas = Empresa.objects.prefetch_related("plazas_curso__curso", "alumnos")

    # === 3. Filtros dinámicos ===
    if q:
        empresas = empresas.filter(
            Q(nombre__icontains=q)
            | Q(localidad__icontains=q)
            | Q(cif__icontains=q)
            | Q(alumnos__nombre__icontains=q)
            | Q(alumnos__uid__icontains=q)
        ).distinct()

    if estados:
        empresas = empresas.filter(estado__in=estados)

    if cursos:
        # Filtramos por cursos ofertados con plazas > 0
        empresas = empresas.filter(
            plazas_curso__curso__code__in=cursos,
            plazas_curso__plazas__gt=0
        ).distinct()

    # === 4. Orden personalizado por estado + nombre ===
    estado_order = {"verde": 0, "naranja": 1, "rojo": 2}
    empresas = sorted(
        empresas,
        key=lambda e: (estado_order.get(e.estado, 99), e.nombre.lower())
    )

    # === 5. Preparar información de plazas y alumnos por empresa ===
    for e in empresas:
        e.plazas_info = []
        for p in e.plazas_curso.all():
            if p.plazas > 0:
                num_alumnos = e.alumnos.filter(curso=p.curso.nombre).count()
                e.plazas_info.append({
                    "curso_nombre": p.curso.nombre,
                    "plazas": p.plazas,
                    "ocupadas": num_alumnos,
                })

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
        "estados": [
            ("verde", "Colabora"),
            ("naranja", "En contacto"),
            ("rojo", "No colabora"),
        ],
        "estados_seleccionados": estados,
        "cursos_seleccionados": cursos,
        "busqueda": q or "",
        "resumen_cursos": resumen_cursos,
    }

    return render(request, "empresas/lista.html", context)




@csrf_exempt
def nueva_empresa(request):
    test_profesor(request)
    if request.method == "POST":
        form = EmpresaForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("empresas:lista")
    else:
        form = EmpresaForm()
    return render(request, "empresas/form.html", {"form": form})


@csrf_exempt
def editar_empresa(request, pk):
    test_profesor(request)
    empresa = get_object_or_404(Empresa, pk=pk)
    if request.method == "POST":
        form = EmpresaForm(request.POST, instance=empresa)
        if form.is_valid():
            form.save()
            return redirect("empresas:lista")
    else:
        form = EmpresaForm(instance=empresa)
    return render(request, "empresas/form.html", {"form": form})

@csrf_exempt
def borrar_empresa(request, pk):
    test_profesor(request)
    empresa = get_object_or_404(Empresa, pk=pk)

    if request.method == "POST":
        empresa.delete()
        return redirect("empresas:lista")

    return render(request, "empresas/confirm_delete.html", {"object": empresa})


@csrf_exempt
def historial_empresa(request, pk):
    """
    Muestra y gestiona el historial de contactos de una empresa.
    - Añadir registros con fecha, hora y descripción.
    - Guardar el profesor logueado desde LDAP.
    - Permitir borrar entradas individuales.
    """
    test_profesor(request)
    empresa = get_object_or_404(Empresa, pk=pk)
    ldap = LibLDAP()

    # === Procesamiento POST (añadir o borrar) ===
    if request.method == "POST":
        if "borrar" in request.POST:
            # Borrar registro concreto
            contacto_id = request.POST.get("borrar")
            HistorialContacto.objects.filter(pk=contacto_id, empresa=empresa).delete()
        else:
            # Crear nuevo registro
            fecha_str = request.POST.get("fecha")
            texto = request.POST.get("texto", "").strip()
    
            if texto:
                # Intentar convertir la fecha desde el input
                try:
                    fecha = timezone.datetime.fromisoformat(fecha_str)
                except Exception:
                    fecha = timezone.now()

                # Obtener profesor desde LDAP
                profesor_username = request.session.get("username", "desconocido")
                profesor_nombre = profesor_username  # valor por defecto

                try:
                    entradas = ldap.buscar(f"(uid={profesor_username})", ["cn"])
                    if entradas:
                        profesor_nombre = entradas[0].get("cn", [profesor_username])[0]
                except Exception:
                    pass

                # Guardar el registro
                HistorialContacto.objects.create(
                    empresa=empresa,
                    profesor_username=profesor_username,
                    profesor_nombre=profesor_nombre,
                    fecha=fecha,
                    texto=texto
                )

        return redirect("empresas:historial", pk=empresa.pk)

    # === En GET: mostrar historial ===
    historial = HistorialContacto.objects.filter(empresa=empresa).order_by('-fecha')

    return render(request, "empresas/historial.html", {
        "empresa": empresa,
        "historial": historial,
        "ahora": timezone.localtime(timezone.now()).strftime("%Y-%m-%dT%H:%M"),
    })
# empresas/views.py (debajo de las vistas)
def _guardar_alumnos(empresa, uids):
    from usuarios.libldap import LibLDAP
    ldap = LibLDAP()

    def curso_de(uid):
        CURSOS = {
            "1SMR": "smr1",
            "2SMR": "smr2",
            "1ASIR": "asir1",
            "2ASIR": "asir2",
        }
        for nombre_curso, grupo in CURSOS.items():
            grupos = ldap.buscar(f"(cn={grupo})", ['member'], base_dn=ldap.group_dn)
            for g in grupos:
                for miembro in g.get("member", []):
                    if f"uid={uid}," in miembro:
                        return nombre_curso
        return ""

    for uid in uids:
        entradas = ldap.buscar(f"(uid={uid})", ['uid','cn'])
        nombre = entradas[0].get("cn", [""])[0] if entradas else uid
        curso = curso_de(uid)

        AlumnoEmpresa.objects.create(
            empresa=empresa,
            uid=uid,
            nombre=nombre,
            curso=curso
        )

# === Alumnos ===
@csrf_exempt
def gestionar_alumnos(request, pk):
    test_profesor(request)
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

    CURSO_TO_LDAP_GROUP = {
        "1SMR": "smr1",
        "2SMR": "smr2",
        "1ASIR": "asir1",
        "2ASIR": "asir2",
    }

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

        grupos = ldap.buscar(f"(cn={grupo})", ['member'], base_dn=ldap.group_dn)
        for g in grupos:
            for miembro in g.get("member", []):
                if not miembro.startswith("uid="):
                    continue
                uid = miembro.split(",")[0].split("=")[1]
                if uid in vistos:
                    continue
                vistos.add(uid)

                entradas = ldap.buscar(f"(uid={uid})", ['uid', 'cn', 'mail'])
                if not entradas:
                    continue
                e = entradas[0]

                uid_norm = (uid or "").lower()
                seguimiento_activo = uid_norm in uids_con_seguimiento
                empresa_asignada = AlumnoEmpresa.objects.filter(uid=uid).exclude(empresa=empresa).first()
                nombre_empresa = empresa_asignada.empresa.nombre if empresa_asignada else ""

                alumno_existente = alumnos.filter(uid=uid).first()

                disponibles.append({
                    "uid": uid,
                    "nombre": e.get("cn", [""])[0],
                    "email": e.get("mail", [""])[0],
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

    from django.contrib import messages

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

        return redirect("empresas:lista")


    # === 5. Renderizar plantilla ===
    return render(request, "empresas/alumnos.html", {
        "empresa": empresa,
        "disponibles": disponibles,
    })

# === Contactos ===
@csrf_exempt
def gestionar_contactos(request, pk):
    test_profesor(request)
    empresa = get_object_or_404(Empresa, pk=pk)

    if request.method == "POST":
        # Alta de un nuevo contacto
        nombre = request.POST.get("nombre", "").strip()
        telefono = request.POST.get("telefono", "").strip()
        email = request.POST.get("email", "").strip()
        if nombre:
            PersonaContacto.objects.create(
                empresa=empresa,
                nombre=nombre,
                telefono=telefono,
                email=email
            )
        return redirect("empresas:contactos", pk=empresa.pk)

    contactos = PersonaContacto.objects.filter(empresa=empresa)
    return render(request, "empresas/contactos.html", {
        "empresa": empresa,
        "contactos": contactos
    })

@csrf_exempt
def borrar_contacto(request, contacto_id):
    test_profesor(request)
    contacto = get_object_or_404(PersonaContacto, pk=contacto_id)
    empresa = contacto.empresa
    contacto.delete()
    return redirect("empresas:contactos", pk=empresa.pk)

# ==seguimiento

@csrf_exempt
def historial_alumno(request, alumno_id):
    """
    Muestra y gestiona el historial de seguimiento de un alumno.
    - Añadir registros con fecha, hora y observación.
    - Guardar el profesor logueado desde LDAP.
    - Permitir borrar entradas individuales.
    """
    test_profesor(request)
    alumno = get_object_or_404(AlumnoEmpresa, pk=alumno_id)
    empresa = alumno.empresa
    ldap = LibLDAP()

    # === Procesamiento POST (añadir o borrar) ===
    if request.method == "POST":
        if "borrar" in request.POST:
            # Borrar registro concreto
            registro_id = request.POST.get("borrar")
            HistorialAlumno.objects.filter(pk=registro_id, alumno=alumno).delete()

        else:
            # Crear nuevo registro
            fecha_str = request.POST.get("fecha")
            texto = request.POST.get("texto", "").strip()

            if texto:
                # Intentar convertir la fecha desde el input
                try:
                    fecha = timezone.datetime.fromisoformat(fecha_str)
                except Exception:
                    fecha = timezone.now()

                # Obtener profesor desde LDAP
                profesor_username = request.session.get("username", "desconocido")
                profesor_nombre = profesor_username  # valor por defecto

                try:
                    entradas = ldap.buscar(f"(uid={profesor_username})", ["cn"])
                    if entradas:
                        profesor_nombre = entradas[0].get("cn", [profesor_username])[0]
                except Exception:
                    pass

                # Guardar el registro
                HistorialAlumno.objects.create(
                    alumno=alumno,
                    profesor_username=profesor_username,
                    profesor_nombre=profesor_nombre,
                    fecha=fecha,
                    texto=texto,
                )

        return redirect("empresas:historial_alumno", alumno_id=alumno.id)

    # === En GET: mostrar historial ===
    historial = HistorialAlumno.objects.filter(alumno=alumno).order_by("-fecha")

    return render(request, "empresas/historial_alumno.html", {
        "empresa": empresa,
        "alumno": alumno,
        "historial": historial,
        "ahora": timezone.localtime(timezone.now()).strftime("%Y-%m-%dT%H:%M"),
    })
