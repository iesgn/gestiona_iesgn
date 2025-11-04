from django import forms
from .models import Empresa, Curso, Empresa, PlazaCurso
from usuarios.libldap import LibLDAP



class EmpresaForm(forms.ModelForm):
    class Meta:
        model = Empresa
        fields = [
            "nombre", "cif", "direccion", "localidad",
            "nif_responsable", "nombre_responsable",
            "profesor_responsable",
            "estado"
        ]
        widgets = {
            "nombre": forms.TextInput(attrs={"class": "form-control"}),
            "cif": forms.TextInput(attrs={"class": "form-control"}),
            "direccion": forms.TextInput(attrs={"class": "form-control"}),
            "localidad": forms.TextInput(attrs={"class": "form-control"}),
            "nif_responsable": forms.TextInput(attrs={"class": "form-control"}),
            "nombre_responsable": forms.TextInput(attrs={"class": "form-control"}),
            "profesor_responsable": forms.TextInput(attrs={"class": "form-control"}), 
            "estado": forms.Select(attrs={"class": "form-control"}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Solo el campo "nombre" es obligatorio
        for field_name, field in self.fields.items():
            if field_name != "nombre":
                field.required = False

        # Crear dinámicamente un campo select por cada curso
        self.cursos = Curso.objects.all()
        for curso in self.cursos:
            field_name = f"plazas_{curso.code}"
            self.fields[field_name] = forms.TypedChoiceField(
                label=f"{curso.nombre}",
                choices=[(i, str(i)) for i in range(0, 11)],  # 0–10 plazas
                coerce=int,
                initial=self.get_plazas_inicial(curso),
                widget=forms.Select(
                    attrs={"class": "form-control input-sm", "style": "width:80px; display:inline-block; margin-left:10px;"}
                )
            )

    def get_plazas_inicial(self, curso):
        """Devuelve las plazas existentes para un curso dado."""
        if not self.instance.pk:
            return 0
        try:
            return PlazaCurso.objects.get(empresa=self.instance, curso=curso).plazas
        except PlazaCurso.DoesNotExist:
            return 0

    def save(self, commit=True):
        instance = super().save(commit)
        for curso in self.cursos:
            plazas = int(self.cleaned_data.get(f"plazas_{curso.code}", 0))
            pc, created = PlazaCurso.objects.get_or_create(empresa=instance, curso=curso)
            if plazas > 0:
                pc.plazas = plazas
                pc.save()
            else:
                pc.delete()
        return instance






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
