import os
import requests
from datetime import datetime, timedelta, timezone
from usuarios.libldap import LibLDAP
from django.shortcuts import render
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings
from gestiona_iesgn.views import test_login


HEADSCALE_URL = os.environ.get("HEADSCALE_URL", "https://vpn.gonzalonazareno.org")
API_BASE = f"{HEADSCALE_URL}/api/v1"


def _headscale_headers():
    api_key = os.environ.get("HEADSCALE_API_KEY", "")
    return {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
    }


def get_headscale_user(username):
    """
    Busca un usuario en Headscale por su nombre.
    Devuelve el dict completo del usuario (incluye 'id') o None si no existe.
    """
    response = requests.get(
        f"{API_BASE}/user",
        headers=_headscale_headers(),
        timeout=10,
    )
    if response.status_code == 401:
        raise PermissionError(
            "Error 401: la HEADSCALE_API_KEY no es válida o no está configurada."
        )
    response.raise_for_status()

    data = response.json()
    users = data.get("users") or data.get("user") or []
    if isinstance(users, dict):
        users = [users]

    for user in users:
        if user.get("name") == username or user.get("username") == username:
            return user
    return None


def delete_old_preauth_keys(user_id):
    """
    Elimina todas las preauth keys del usuario antes de crear una nueva.
    """
    response = requests.get(
        f"{API_BASE}/preauthkey",
        headers=_headscale_headers(),
        timeout=10,
    )
    if not response.ok:
        return

    data = response.json()
    keys = data.get("preAuthKeys") or data.get("preAuthKey") or []
    if isinstance(keys, dict):
        keys = [keys]

    for k in keys:
        # Filtrar solo las keys del usuario que hace la solicitud
        if k.get("user", {}).get("id") != str(user_id):
            continue
        key_id = k.get("id")
        if not key_id:
            continue
        requests.delete(
            f"{API_BASE}/preauthkey?id={key_id}",
            headers=_headscale_headers(),
            timeout=10,
        )

def create_preauth_key(user_id):
    """
    Crea una preauth key de un solo uso, válida 24h, para el user_id numérico dado.
    """
    expiration = datetime.now(timezone.utc) + timedelta(hours=24)
    payload = {
        "user": str(user_id),
        "reusable": False,
        "ephemeral": False,
        "expiration": expiration.strftime("%Y-%m-%dT%H:%M:%SZ"),
        "aclTags": [],
    }
    response = requests.post(
        f"{API_BASE}/preauthkey",
        headers=_headscale_headers(),
        json=payload,
        timeout=10,
    )
    if response.status_code == 401:
        raise PermissionError(
            "Error 401: la HEADSCALE_API_KEY no es válida o no está configurada."
        )
    if not response.ok:
        raise ValueError(
            f"Error {response.status_code} al crear la preauth key: {response.text}"
        )

    data = response.json()
    preauth = data.get("preAuthKey") or data.get("pre_auth_key") or {}
    return preauth.get("key")


def solicitar_vpn(request):
    test_login(request)
    username = request.session["username"]

    if request.method == "POST":

        # 1. Comprobar que el usuario existe en Headscale
        try:
            headscale_user = get_headscale_user(username)
        except PermissionError as e:
            messages.error(request, str(e))
            return render(request, "solicitar.html")
        except requests.RequestException as e:
            messages.error(request, f"No se pudo conectar con el servidor VPN: {e}")
            return render(request, "solicitar.html")

        if headscale_user is None:
            messages.error(
                request,
                f"El usuario '{username}' no está registrado en el servidor VPN. "
                "Contacta con el administrador para que te den de alta.",
            )
            return render(request, "solicitar.html")

        # 2. Expirar keys anteriores sin usar y crear una nueva
        try:
            user_id = headscale_user.get("id")
            delete_old_preauth_keys(user_id)
            auth_key = create_preauth_key(user_id)
        except (PermissionError, ValueError) as e:
            messages.error(request, str(e))
            return render(request, "solicitar.html")
        except requests.RequestException as e:
            messages.error(request, f"No se pudo generar la clave de acceso: {e}")
            return render(request, "solicitar.html")

        if not auth_key:
            messages.error(
                request,
                "La API de Headscale no devolvió ninguna clave. "
                "Inténtalo de nuevo o contacta con el administrador.",
            )
            return render(request, "solicitar.html")

        # 3. Obtener email del LDAP
        ldap = LibLDAP()
        resultado = ldap.buscar(f"(uid={username})", ["mail"])
        if not resultado or not resultado[0].get("mail"):
            messages.error(
                request,
                "No se encontró dirección de correo en el LDAP para tu usuario. "
                "Contacta con el administrador.",
            )
            return render(request, "solicitar.html")
        user_email = resultado[0]["mail"][0]

        # 4. Enviar correo con la key e instrucciones
        asunto = "Tu clave de acceso a la VPN del IES Gonzalo Nazareno"
        cuerpo = f"""Hola {username},

Has solicitado acceso a la VPN del IES Gonzalo Nazareno mediante Tailscale.

Tu AUTH KEY (válida durante 24 horas):

    {auth_key}

────────────────────────────────────────
INSTRUCCIONES DE REGISTRO
────────────────────────────────────────

1. Instala el cliente Tailscale en tu dispositivo:
   https://tailscale.com/download

Para sistemas Linux:

curl -fsSL https://tailscale.com/install.sh | sh

Tienes clientes Tailscale para otros sistemas operativos: Windows, Android, iOS.

2. Conéctate al servidor VPN del centro ejecutando:

   Linux:
     sudo tailscale up --accept-routes --login-server {HEADSCALE_URL} --authkey {auth_key}

Cuando termines de trabajar con la VPN puedes desconectarla con:

sudo tailscale down

Posteriormente para volver a trabajar con la VPN, solo es necesario ejecutar:

sudo tailscale up

3. Una vez conectado, podrás acceder a los recursos de la red del centro. Prueba a acceder a nuestro router:

ping 172.22.0.1

IMPORTANTE:
  · Esta clave es de un solo uso y caduca en 24 horas.
  · No la compartas con nadie.
  · Si tienes problemas, contacta con el administrador.

──────────────────────────────────────
IES Gonzalo Nazareno - Servicio de Informática
"""

        try:
            send_mail(
                asunto,
                cuerpo,
                settings.DEFAULT_FROM_EMAIL,
                [user_email],
                fail_silently=False,
            )
            messages.success(
                request,
                f"Se ha generado una nueva auth key y se ha enviado a {user_email}. "
                "Revisa tu bandeja de entrada (y el spam).",
            )
        except Exception as e:
            messages.error(
                request,
                f"Se generó la clave pero no se pudo enviar el correo: {e}. "
                "Contacta con el administrador.",
            )

        return render(request, "solicitar.html")

    return render(request, "solicitar.html")