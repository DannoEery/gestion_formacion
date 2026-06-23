from django.urls import path
from .views import matricularse
from .views import (
    matricularse,
    mis_cursos,
    DashboardAlumnoView,
    cancelar_matricula
)

# Lista que define los patrones de URL para esta aplicación específica
urlpatterns = [
    # Ruta para el proceso de inscripción a un curso
    path(
        'matricular/<int:curso_id>/', # URL del navegador. <int:curso_id> captura el ID de la URL y lo pasa como entero a la vista
        matricularse,                 # La función de la vista que se ejecutará al visitar esta URL
        name='matricularse'           # Nombre único de la ruta para poder llamarla desde plantillas (templates) o redirecciones
    ),
    path(
        'mis-cursos/',
        mis_cursos,
        name='mis_cursos'
    ),
    path(
        'dashboard/',
        DashboardAlumnoView.as_view(),
        name='dashboard'
    ),

    path(
        'cancelar/<int:matricula_id>/',
        cancelar_matricula,
        name='cancelar_matricula'
    ),
]

