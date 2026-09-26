from django.urls import path
from . import views

app_name = "empresas"

urlpatterns = [
    path("", views.lista_empresas, name="lista"),
    path("nueva/", views.nueva_empresa, name="crear"),
    path("historial-dual/", views.historial_dual_view, name="historial_dual"),
    path("listado/", views.listado_empresas, name="listado"),
    path("sin-empresa/", views.alumnos_sin_empresa, name="sin_empresa"),
    path("<int:pk>/editar/", views.editar_empresa, name="editar"),
    path("<int:pk>/borrar/", views.borrar_empresa, name="borrar"),
    path("<int:pk>/historial/", views.historial_empresa, name="historial"),
    # Nuevas acciones:
    path('<int:pk>/alumnos/', views.gestionar_alumnos, name='alumnos'),
    path('<int:pk>/contactos/', views.gestionar_contactos, name='contactos'),
    path('contacto/<int:contacto_id>/editar/', views.editar_contacto, name='editar_contacto'),
    path('contacto/<int:contacto_id>/borrar/', views.borrar_contacto, name='borrar_contacto'),
    path('alumno/<int:alumno_id>/historial/', views.historial_alumno, name='historial_alumno'),

]
