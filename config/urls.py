"""
URL configuration for config project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
# Importa el panel de administración de Django

from django.urls import path, include
# Importa la función path para definir rutas (URLs)

from django.conf import settings
# Importa la configuración global del proyecto (settings.py)
# Permite acceder a variables como MEDIA_URL, MEDIA_ROOT, DEBUG, etc.

from django.conf.urls.static import static
# Función de Django que permite servir archivos media (y estáticos en desarrollo)
# Se usa normalmente junto con MEDIA_URL y MEDIA_ROOT cuando DEBUG=True


urlpatterns = [
# Lista principal de rutas del proyecto (nivel global)

    path(
        'admin/',
        # Ruta que comienza con /admin/

        admin.site.urls
        # Activa el panel de administración de Django
    ),

    path(
        '',
        # Ruta vacía: representa la página principal del sitio

        include('core.urls')
        # Incluye todas las rutas definidas en la app "core"
        # Es decir, delega el manejo de URLs a core/urls.py
    ),

    path(
        'usuarios/',
        include('usuarios.urls')
    ),
# URLs de la app usuarios → /usuarios/...


    path(
        'accounts/',
        include(
            'django.contrib.auth.urls'
        )
    ),
# URLs de autenticación de Django (login, logout, reset password)
# Ej: /accounts/login/ → permite usar redirect('login')

    path(
        'cursos/',
        include(
            'cursos.urls'
        )
    ),

    path(
        'matriculas/',
        include(
            'matriculas.urls')
    ),
]
# Fin de las rutas globales del proyecto
if settings.DEBUG:
    # Comprueba si el proyecto está en modo desarrollo (DEBUG = True)
    # Esto evita que se sirvan archivos media en producción de esta forma

    urlpatterns += static(
        settings.MEDIA_URL,
        document_root=settings.MEDIA_ROOT
    )
    # Añade rutas automáticas para servir archivos multimedia (MEDIA)
    # MEDIA_URL → URL pública (/media/)
    # MEDIA_ROOT → carpeta real donde están los archivos subidos
    # Esto permite ver imágenes subidas durante el desarrollo
