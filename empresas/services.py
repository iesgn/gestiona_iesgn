from typing import List, Dict
from usuarios.libldap import LibLDAP

# Mapeo local Curso.code -> nombre de grupo LDAP (según usuarios.libldap.LibLDAP.grupos keys)
CURSO_TO_LDAP_GROUP = {
    "1SMR": "smr1",
    "2SMR": "smr2",
    "1ASIR": "asir1",
    "2ASIR": "asir2",
}


def alumnos_de_empresa(empresa) -> List[Dict]:
    """
    Devuelve una lista de alumnos asociados a los cursos de la empresa,
    consultando el servidor LDAP.
    """
    ldap = LibLDAP()

    results = []

    for curso in empresa.cursos.all():
        grupo = CURSO_TO_LDAP_GROUP.get(curso.code)
        if not grupo:
            continue

        # Buscar el grupo LDAP y extraer miembros
        grupos = ldap.buscar(f"(cn={grupo})", ['cn', 'member'], base_dn=ldap.group_dn)
        miembros_dns = []
        for g in grupos:
            miembros_dns.extend(g.get("member", []))

        for dn in miembros_dns:
            if not dn.startswith("uid="):
                continue
            uid = dn.split(",")[0].split("=")[1]
            entries = ldap.buscar(f"(uid={uid})", ['uid', 'cn', 'mail'], base_dn=ldap.base_dn)
            if entries:
                e = entries[0]
                results.append({
                    "uid": e.get("uid", [""])[0],
                    "cn": e.get("cn", [""])[0],
                    "mail": e.get("mail", [""])[0],
                    "grupos": ldap.memberOfGroup(uid),
                })

    # Eliminar duplicados por uid
    uniq = {}
    for x in results:
        uniq[x["uid"]] = x
    return list(uniq.values())
