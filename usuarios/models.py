from django.contrib.auth.models import AbstractUser
# Importa el modelo base de usuario de Django (AbstractUser)
# Permite crear un usuario personalizado manteniendo todo el sistema de autenticación de Django

from django.db import models
# Importa las herramientas de Django para crear modelos (tablas de base de datos)


# Create your models here.

class Usuario(AbstractUser):
    # Creamos un modelo personalizado de usuario que hereda de AbstractUser
    # Esto nos permite añadir campos extra al usuario sin perder login, permisos, etc.

    TIPO_USUARIO = (
        ('alumno', 'Alumno'),
        # Opción 1 del campo tipo: el usuario es un alumno

        ('profesor', 'Profesor'),
        # Opción 2 del campo tipo: el usuario es un profesor

        ('administrador', 'Administrador'),
    )

    tipo = models.CharField(
        max_length=20,
        choices=TIPO_USUARIO,
        default='alumno'
    )
    # Campo que indica el tipo de usuario
    # CharField = campo de texto corto
    # choices = limita los valores a "alumno" o "profesor"
    # default = si no se especifica, será "alumno"

    def __str__(self):
        # Método que define cómo se muestra el objeto Usuario en el admin o consola

        return self.username
        # Devuelve el nombre de usuario como representación del objeto

