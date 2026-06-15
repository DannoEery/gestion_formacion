from django.urls import path
# Importa la función path, que se usa para definir rutas (URLs) en Django

from .views import (
    lista_cursos,
    detalle_curso
)
# Importa las vistas que van a manejar las URLs:
# - lista_cursos: muestra todos los cursos
# - detalle_curso: muestra un curso concreto

urlpatterns = [
    # Lista de rutas de la aplicación cursos

    path(
        '',
        # Ruta vacía: página principal de la app cursos (/cursos/)

        lista_cursos,
        # Vista que se ejecuta para mostrar la lista de cursos

        name='lista_cursos'
        # Nombre de la ruta para usar en templates ({% url 'lista_cursos' %})
    ),

    path(
        '<int:curso_id>/',
        # Ruta dinámica: recibe un número entero como ID del curso
        # Ejemplo: /cursos/3/

        detalle_curso,
        # Vista que muestra el detalle del curso seleccionado

        name='detalle_curso'
        # Nombre de la ruta para enlazarla desde templates
    ),
]