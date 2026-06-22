from django.db import models
# Importa el sistema de modelos de Django (ORM)

from profesores.models import Profesor
# Importa el modelo Profesor para poder relacionarlo con Curso

from django.core.exceptions import ValidationError
# Permite lanzar errores de validación en los modelos

class Curso(models.Model):
    # Modelo que representa un curso dentro de la plataforma

    nombre = models.CharField(
        max_length=200
    )
    # Nombre del curso (texto corto, máximo 200 caracteres)

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

    def __str__(self):
        # Representación en texto del objeto Curso

        return self.nombre
        # Muestra el nombre del curso en el admin y en relaciones