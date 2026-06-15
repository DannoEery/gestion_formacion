from django.urls import path
# Importa la función path para definir rutas (URLs) en Django

from .views import registro
# Importa la vista "registro" desde el archivo views.py de esta aplicación


urlpatterns = [
    # Lista donde se definen todas las rutas de esta app

    path(
        'registro/',
        # URL que se activará cuando el usuario entre a /registro/

        registro,
        # Vista que se ejecutará cuando se acceda a esta URL

        name='registro'
        # Nombre de la ruta, se usa en templates con {% url 'registro' %}
    ),
]