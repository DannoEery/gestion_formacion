# Importa la función redirect para redirigir al usuario a otra URL
from django.shortcuts import redirect
# Importa el sistema de mensajes de Django para mostrar alertas en la interfaz
from django.contrib import messages


# Define un decorador personalizado para restringir el acceso solo a profesores
def profesor_required(view_func):

    # Define la función interna que envolverá a la vista original
    def wrapper(request, *args, **kwargs):

        # Comprueba si el usuario actual NO ha iniciado sesión
        if not request.user.is_authenticated:
            # Redirige al usuario a la página con el nombre de URL 'login'
            return redirect('login')

        # Comprueba si el rol del usuario autenticado NO es 'profesor'
        if request.user.tipo != 'profesor':
            # Añade un mensaje de error que se mostrará al usuario en la siguiente pantalla
            messages.error(
                request,
                'Acceso denegado.'
            )
            # Redirige al usuario a la página de inicio del sitio
            return redirect('inicio')

        # Si pasa ambas validaciones, ejecuta y retorna la vista original con sus argumentos
        return view_func(
            request,
            *args,
            **kwargs
        )

    # Retorna la función interna configurada para proteger la vista
    return wrapper
