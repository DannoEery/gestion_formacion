from django.db import models

# Importa el sistema de modelos de Django para crear tablas en la base de datos

from django.conf import settings

# Permite acceder a configuraciones del proyecto, como AUTH_USER_MODEL


# Create your models here.
# Aquí se definen los modelos que se convertirán en tablas de la base de datos


class Profesor(models.Model):
    # Modelo que representa a un profesor dentro del sistema
    # Cada instancia de esta clase será un registro en la base de datos

    usuario = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        # Relación uno a uno con el modelo de usuario personalizado de Django
        on_delete=models.CASCADE,
        # Si el usuario se elimina, también se elimina el profesor asociado
        related_name="profesor",
        # Permite acceder desde el usuario con: usuario.profesor
    )

    especialidad = models.CharField(max_length=100)
    # Campo de texto corto para guardar la especialidad del profesor
    # Ejemplo: "Matemáticas", "Programación", etc.

    telefono = models.CharField(max_length=20)
    # Campo de texto para almacenar el número de teléfono

    biografia = models.TextField(blank=True)
    # Campo de texto largo para la biografía del profesor
    # blank=True permite que pueda estar vacío en formularios

    foto = models.ImageField(upload_to="profesores/", blank=True, null=True)
    # Campo para subir imágenes
    # upload_to='profesores/' guarda las imágenes en esa carpeta
    # blank=True permite dejarlo vacío en formularios
    # null=True permite valores nulos en la base de datos

    def __str__(self):
        # Método que define cómo se muestra el objeto en el admin o consola

        return f"{self.usuario.first_name} " f"{self.usuario.last_name}"
        # Devuelve el nombre completo del profesor usando el usuario asociado
