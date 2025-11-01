from django.urls import path
from . import views

app_name = "empresas"

urlpatterns = [
    path("", views.lista_empresas, name="lista"),
    path("nueva/", views.nueva_empresa, name="crear"),
    path("<int:pk>/editar/", views.editar_empresa, name="editar"),
    path("<int:pk>/borrar/", views.borrar_empresa, name="borrar"),
    path("<int:pk>/historial/", views.historial_empresa, name="historial"),
    # Nuevas acciones:
    path('<int:pk>/alumnos/', views.gestionar_alumnos, name='alumnos'),
    path('<int:pk>/contactos/', views.gestionar_contactos, name='contactos'),
    path('contacto/<int:contacto_id>/borrar/', views.borrar_contacto, name='borrar_contacto'),
    path('alumno/<int:alumno_id>/historial/', views.historial_alumno, name='historial_alumno'),

]
