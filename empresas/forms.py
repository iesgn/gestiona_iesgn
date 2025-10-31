from django import forms
from .models import Empresa, Curso
from usuarios.libldap import LibLDAP

class EmpresaForm(forms.ModelForm):
    cursos = forms.ModelMultipleChoiceField(
        queryset=Curso.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False,
        label="Cursos"
    )

    class Meta:
        model = Empresa
        fields = [
            "cif", "nombre", "direccion", "localidad",
            "nif_responsable", "nombre_responsable",
            "estado", "cursos"
        ]




    def obtener_alumnos_de_cursos(self, cursos):
        ldap = LibLDAP()
        opciones = []
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
            grupos = ldap.buscar(f"(cn={grupo})", ['cn', 'member'], base_dn=ldap.group_dn)
            for g in grupos:
                for dn in g.get("member", []):
                    if not dn.startswith("uid="):
                        continue
                    uid = dn.split(",")[0].split("=")[1]
                    entradas = ldap.buscar(f"(uid={uid})", ['uid', 'cn'])
                    if entradas:
                        e = entradas[0]
                        nombre = e.get("cn", [""])[0]
                        opciones.append((uid, f"{nombre} ({curso.nombre})"))
        return sorted(opciones, key=lambda x: x[1])
