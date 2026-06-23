# Importa la función path para definir rutas de URL individuales en Django
from django.urls import path
# Importa la vista del panel de control que creamos para el profesor
from .views import dashboard_profesor, mis_cursos_profesor


# Lista que almacena todas las rutas de URL accesibles para este módulo
urlpatterns = [
    # Define la ruta web que conecta la URL con la vista del profesor
    path(
        # El subdominio o texto que el usuario verá en el navegador (ej: ://tusitio.com)
        'dashboard/',
        # La función de la vista que Django ejecutará cuando se visite esta URL
        dashboard_profesor,
        # El nombre único de la ruta para poder referenciarla en plantillas o redirecciones
        name='dashboard_profesor'
    ),
    path(
        'mis-cursos/',
        mis_cursos_profesor,
        name='mis_cursos_profesor'
    ),
]
