from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy
from django.db.models import Q
from gestiona_iesgn.views import test_profesor
from .forms import EmpresaForm
from .models import Empresa, PersonaContacto, AlumnoEmpresa, HistorialContacto,Curso
from .services import alumnos_de_empresa
from usuarios.libldap import LibLDAP
from django.utils import timezone


@csrf_exempt
def lista_empresas(request):
    test_profesor(request)

    q = request.GET.get("q")
    estados = request.GET.getlist("estado")
    cursos = request.GET.getlist("curso")

    empresas = Empresa.objects.prefetch_related("cursos")

    if q:
        empresas = empresas.filter(
            Q(nombre__icontains=q)
            | Q(localidad__icontains=q)
            | Q(cif__icontains=q)
        )

    if estados:
        empresas = empresas.filter(estado__in=estados)

    if cursos:
        empresas = empresas.filter(cursos__code__in=cursos).distinct()

    # Orden: verde → naranja → rojo
    estado_order = {"verde": 0, "naranja": 1, "rojo": 2}
    empresas = sorted(empresas, key=lambda e: (estado_order.get(e.estado, 99), e.nombre.lower()))

    context = {
        "object_list": empresas,
        "cursos": Curso.objects.all(),
        "estados": [
            ("verde", "Colabora"),
            ("naranja", "En contacto"),
            ("rojo", "No colabora"),
        ],
        # 👇 Añadimos las selecciones actuales
        "estados_seleccionados": estados,
        "cursos_seleccionados": cursos,
        "busqueda": q or "",
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

    # === 1. Obtener cursos y alumnos actuales ===
    cursos = empresa.cursos.all()
    alumnos = AlumnoEmpresa.objects.filter(empresa=empresa)
    existentes = [a.uid for a in alumnos]

    # === 2. Buscar alumnos en LDAP según cursos ===
    disponibles = []
    CURSO_TO_LDAP_GROUP = {
        "1SMR": "smr1",
        "2SMR": "smr2",
        "1ASIR": "asir1",
        "2ASIR": "asir2",
    }

    for curso in cursos:
        grupo = CURSO_TO_LDAP_GROUP.get(curso.code)
        if not grupo:
            continue
        grupos = ldap.buscar(f"(cn={grupo})", ['member'], base_dn=ldap.group_dn)
        for g in grupos:
            for miembro in g.get("member", []):
                if not miembro.startswith("uid="):
                    continue
                uid = miembro.split(",")[0].split("=")[1]
                entradas = ldap.buscar(f"(uid={uid})", ['uid', 'cn', 'mail'])
                if entradas:
                    e = entradas[0]
                    # Comprobar si el alumno está asignado a alguna empresa
                    empresa_asignada = AlumnoEmpresa.objects.filter(uid=uid).exclude(empresa=empresa).first()
                    nombre_empresa = empresa_asignada.empresa.nombre if empresa_asignada else ""
                    
                    disponibles.append({
                        "uid": uid,
                        "nombre": e.get("cn", [""])[0],
                        "email": e.get("mail", [""])[0],
                        "curso": curso.nombre,
                        "seleccionado": uid in existentes,
                        "fuera_de_curso": False,
                        "empresa_asignada": nombre_empresa,
                    })
                    

    # === 3. Añadir alumnos guardados que ya no están en los cursos actuales ===
    uids_ldap = {a["uid"] for a in disponibles}
    for guardado in alumnos:
        if guardado.uid not in uids_ldap:
            disponibles.append({
                "uid": guardado.uid,
                "nombre": guardado.nombre or guardado.uid,
                "email": "",
                "curso": guardado.curso or "—",
                "seleccionado": True,
                "fuera_de_curso": True,
            })

    # === 4. Procesar guardado ===
    if request.method == "POST":
        seleccionados = request.POST.getlist("alumnos")

        # Eliminar los que no están seleccionados
        AlumnoEmpresa.objects.filter(empresa=empresa).exclude(uid__in=seleccionados).delete()

        # Crear o actualizar los seleccionados
        for a in disponibles:
            if a["uid"] in seleccionados:
                AlumnoEmpresa.objects.update_or_create(
                    empresa=empresa,
                    uid=a["uid"],
                    defaults={
                        "nombre": a["nombre"],
                        "curso": a["curso"],
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