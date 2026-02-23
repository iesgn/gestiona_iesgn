from django.urls import path
from . import views

app_name = "vpn"

urlpatterns = [
    path("", views.solicitar_vpn, name="solicitar"),
]
