from django.urls import re_path
from . import views

app_name = "empresas"

urlpatterns = [
    re_path(r'^$', views.lista_empresas, name="lista"),
    re_path(r'^nueva/', views.nueva_empresa, name="crear"),
    re_path(r'^<int:pk>/editar/', views.editar_empresa, name="editar"),
    re_path(r'^<int:pk>/borrar/', views.borrar_empresa, name="borrar"),
    re_path(r'^<int:pk>/historial/', views.historial_empresa, name="historial"),
    # Nuevas acciones:
    re_path(r'^<int:pk>/alumnos/', views.gestionar_alumnos, name='alumnos'),
    re_path(r'^<int:pk>/contactos/', views.gestionar_contactos, name='contactos'),
    re_path(r'^contacto/<int:contacto_id>/borrar/', views.borrar_contacto, name='borrar_contacto'),
    re_path(r'^alumno/<int:alumno_id>/historial/', views.historial_alumno, name='historial_alumno'),

]
