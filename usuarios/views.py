from django.shortcuts import render
# Importa la función render para mostrar una plantilla HTML con contexto

from django.shortcuts import redirect
# Importa redirect para redirigir al usuario a otra URL después de una acción

from .forms import RegistroAlumnoForm
# Importa el formulario personalizado de registro de usuarios


# Create your views here.

def registro(request):
    # Vista que maneja el registro de un nuevo usuario

    form = RegistroAlumnoForm(
        request.POST
    )
    # Crea una instancia del formulario con los datos enviados por POST (si existen)

    if form.is_valid():
        # Comprueba si los datos del formulario son válidos según las reglas de Django

        form.save()
        # Guarda el nuevo usuario en la base de datos

        return redirect(
            'login'
        )
        # Redirige al usuario a la página de login después de registrarse correctamente

    else:
        form = RegistroAlumnoForm()
        # Si el formulario no es válido (o es GET), se crea uno vacío para mostrarlo

    return render(
        request,
        'usuarios/registro.html',
        {
            'form': form
        }
    )
    # Renderiza la plantilla registro.html y le pasa el formulario al template