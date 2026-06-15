from django.contrib.auth.forms import UserCreationForm
# Importa el formulario base de Django para crear usuarios
# Ya incluye validaciones como contraseña, repetición de contraseña, etc.

from .models import Usuario
# Importa el modelo personalizado Usuario desde la app actual


class RegistroAlumnoForm(
    UserCreationForm
):
    # Creamos un formulario de registro heredando de UserCreationForm
    # Esto permite registrar usuarios nuevos con contraseña segura

    class Meta:
        # Clase interna que define qué modelo y campos usará el formulario

        model = Usuario
        # Indica que este formulario trabaja con el modelo Usuario personalizado

        fields = (
            'username',
            'first_name',
            'last_name',
            'email',
        )
        # Campos que se mostrarán en el formulario
        # username → nombre de usuario
        # first name → nombre del usuario
        # last name → apellidos del usuario
        # email → correo electrónico del usuario