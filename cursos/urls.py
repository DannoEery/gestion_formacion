from django.urls import path
# Importa la función path para crear URLs

from .views import (
    ListaCursosView,
    detalle_curso
)
# Importa las vistas:
# ListaCursosView -> lista de cursos con CBV
# detalle_curso -> detalle de un curso


urlpatterns = [

    path(
        '',
        # Página principal de cursos

        ListaCursosView.as_view(),
        # Ejecuta la vista basada en clases

        name='lista_cursos'
        # Nombre usado en templates
    ),


    path(
        '<slug:slug>/',
        # URL SEO:
        # ejemplo /cursos/python-basico/

        detalle_curso,
        # Vista del detalle

        name='detalle_curso'
    ),
]