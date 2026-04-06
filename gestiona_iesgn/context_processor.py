import json
import os
from django.conf import settings

def my_site_url(request):
    path = os.path.join(settings.BASE_DIR, 'gestiona_iesgn', 'enlaces.json')
    with open(path, encoding='utf-8') as f:
        config = json.load(f)
    return {
        'SITE_URL': settings.SITE_URL,
        'SITE_URL_STATIC': settings.SITE_URL_STATIC,
        'menu': config['menu'],
    }