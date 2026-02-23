# App `vpn` — Instrucciones de integración

## 1. Copiar la app al proyecto

```
cp -r vpn/ /ruta/a/gestiona_iesgn/
```

## 2. Registrar la app en `gestiona_iesgn/settings.py`

```python
INSTALLED_APPS = [
    ...
    'vpn',
]
```

## 3. Incluir las URLs en `gestiona_iesgn/urls.py`

```python
from django.urls import path, include

urlpatterns = [
    ...
    path('vpn/', include('vpn.urls')),
]
```

## 4. Variables de entorno necesarias

Añade al entorno (fichero `.env`, `docker-compose.yml`, etc.):

```
HEADSCALE_URL=https://vpn.gonzalonazareno.org
HEADSCALE_API_KEY=<tu_api_key_de_headscale>
```

La API key se genera en el servidor Headscale con:
```bash
headscale apikeys create --expiration 365d
```

## 5. Configuración de correo en `settings.py`

La app usa el sistema de correo estándar de Django. Asegúrate de tener configurado:

```python
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.tuservidor.org'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = 'usuario@tudominio.org'
EMAIL_HOST_PASSWORD = os.environ.get('EMAIL_HOST_PASSWORD')
DEFAULT_FROM_EMAIL = 'noreply@gonzalonazareno.org'
```

## 6. Dependencias Python

La app solo usa `requests`, que ya debería estar instalado. Si no:

```bash
pip install requests
```

Añádelo a `requirements.txt`:
```
requests
```

## 7. Enlace en el menú / plantilla base

En la plantilla de menú (p.ej. `templates/t2bloque.html`), añade:

```html
{% if user.is_authenticated %}
<li class="list-group-item list-group-item-action">
  <a href="{% url 'vpn:solicitar' %}">Acceso VPN</a>
</li>
{% endif %}
```

## 8. Flujo de uso

1. El usuario inicia sesión en la aplicación.
2. Accede a `/vpn/`.
3. La vista comprueba que su `username` existe como usuario en Headscale
   (`GET /api/v1/user`).
4. Si existe, crea una preauth key de un solo uso válida 24h
   (`POST /api/v1/preauthkey`).
5. Envía un correo a la dirección del usuario con la key y las instrucciones
   para conectar con `tailscale up --login-server ... --authkey ...`.

## 9. Alta previa del usuario en Headscale

El usuario debe existir previamente en Headscale. El administrador lo crea así:

```bash
headscale users create <username>
```

Si el usuario no existe, la vista muestra un mensaje de error indicándoselo.

## Estructura de archivos

```
vpn/
├── __init__.py
├── apps.py
├── urls.py
├── views.py
└── templates/
    └── vpn/
        └── solicitar.html
```
