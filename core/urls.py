from django.urls import path
# Importa la función path, que se usa para definir rutas (URLs) en Django

from .views import inicio
# Importa la vista llamada "inicio" desde el archivo views.py de esta misma aplicación

urlpatterns = [
# Lista donde se definen todas las rutas (URLs) de la aplicación

    path(
        '',  
        # Ruta vacía '' significa la página principal (home) de la app

        inicio,  
        # Vista que se ejecutará cuando alguien entre a esta URL

        name='inicio'
        # Nombre interno de la ruta.
        # Se usa para referenciarla en plantillas con {% url 'inicio' %}
    ),

]
# Fin de la lista de rutas