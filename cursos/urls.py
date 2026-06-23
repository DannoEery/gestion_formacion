from django.urls import path
# Importa la función path para crear URLs

from .views import (
    ListaCursosView,
    CursoDetailView
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
        CursoDetailView.as_view(),
        name='detalle_curso'
)   ,
]