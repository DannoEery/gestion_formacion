from django.db import models
# Importa el sistema de modelos de Django (ORM)

from profesores.models import Profesor
# Importa el modelo Profesor para poder relacionarlo con Curso

from django.core.exceptions import ValidationError
# Permite lanzar errores de validación en los modelos

# Desde el módulo de utilidades de texto de Django...
from django.utils.text import (
    slugify,
)  # ...importa la función para limpiar y convertir textos en cadenas aptas para URLs (slugs).


class Curso(models.Model):
    # Modelo que representa un curso dentro de la plataforma

    nombre = models.CharField(
    max_length=200,  # Define la longitud máxima permitida para el texto del nombre del curso (200 caracteres).
    db_index=True,  # Crea un índice en la base de datos para este campo, acelerando drásticamente las búsquedas de texto.
    )   
    #Nombre Curso


    slug = models.SlugField(  # Define un campo de texto especializado para almacenar "slugs" (caracteres seguros para URLs).
    unique=True  # Exige que cada registro en la base de datos tenga un slug único; no se permiten duplicados.
    )


    descripcion = models.TextField()
    # Descripción larga del curso

    profesor = models.ForeignKey(
        Profesor,
        on_delete=models.PROTECT,
        related_name='cursos'
    )
    # Relación muchos-a-uno:
    # muchos cursos pueden pertenecer a un profesor
    # PROTECT evita borrar un profesor si tiene cursos asignados
    # related_name='cursos' permite acceder desde profesor.cursos.all()

    fecha_inicio = models.DateField()
    # Fecha en la que empieza el curso

    fecha_fin = models.DateField()
    # Fecha en la que termina el curso

    plazas = models.PositiveIntegerField(
        default=20
    )
    # Número de plazas disponibles (solo valores positivos)

    activo = models.BooleanField(
        default=True
    )
    # Indica si el curso está activo o no

    imagen = models.ImageField(
        upload_to='cursos/',
        blank=True,
        null=True
    )
    # Imagen del curso
    # Se guarda en la carpeta media/cursos/
    # Puede estar vacío (blank/null)

    created_at = models.DateTimeField(
        auto_now_add=True
    )
    # Fecha de creación automática del registro

    updated_at = models.DateTimeField(
        auto_now=True
    )
    # Fecha de última actualización automática

    def clean(self):
        # Método de validación personalizado del modelo
        # Se ejecuta cuando se valida el objeto (por ejemplo en admin o formularios)

        if self.fecha_fin < self.fecha_inicio:
            # Comprueba si la fecha de fin es anterior a la de inicio

            raise ValidationError(
                "La fecha final no puede ser anterior a la inicial"
            )
            # Lanza un error si la regla no se cumple
    def save(self, *args, **kwargs):
    # Sobrescribe el método de guardado estándar de Django para añadir lógica personalizada antes de almacenar los datos.
    # (*args, **kwargs) asegura que el método acepte cualquier argumento adicional requerido por el framework.

        if not self.slug:
            # Verifica si el campo 'slug' se encuentra vacío en el objeto actual.

            self.slug = slugify(self.nombre)
            # Genera automáticamente el slug limpiando el texto del campo 'nombre' y lo asigna al atributo 'slug'.

        super().save(*args, **kwargs)
        # Invoca el método 'save' original de la clase base (models.Model).
        # Este paso es obligatorio para que los cambios se escriban de forma efectiva en la base de datos.

    def __str__(self):
        # Representación en texto del objeto Curso

        return self.nombre
        # Muestra el nombre del curso en el admin y en relaciones