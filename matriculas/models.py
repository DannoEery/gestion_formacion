from django.db import models
from django.conf import settings
from cursos.models import Curso

# Modelo que representa la inscripción de un alumno en un curso
class Matricula(models.Model):
    # Relación muchos a uno (Many-to-One): Un alumno puede tener muchas matrículas
    alumno = models.ForeignKey(
        settings.AUTH_USER_MODEL, # Modelo de usuario personalizado definido en settings.py
        on_delete=models.CASCADE, # Si se elimina el usuario, se eliminan todas sus matrículas
        related_name='matriculas' # Nombre del atributo inverso para acceder desde el usuario (ej: user.matriculas.all())
    )
    # Relación muchos a uno (Many-to-One): Un curso puede tener muchos alumnos matriculados
    curso = models.ForeignKey(
        Curso,                    # Modelo del curso al que pertenece esta matrícula
        on_delete=models.CASCADE, # Si se elimina el curso, se eliminan todas sus matrículas asociadas
        related_name='matriculas' # Nombre del atributo inverso para acceder desde el curso (ej: curso.matriculas.all())
    )
    # Campo de fecha y hora que se autogenera al crear la matrícula
    fecha_matricula = models.DateTimeField(
        auto_now_add=True         # Asigna automáticamente la fecha/hora actual solo al crear el registro
    )
    
    class Meta:
        # Restricción a nivel de base de datos para evitar duplicados
        unique_together = (
            'alumno',             # Un alumno no puede inscribirse en el mismo curso
            'curso'               # ...más de una vez
        )

    # Método que define cómo se representa el objeto como texto (muy útil en el panel de administración)
    def __str__(self):
        return (
            f"{self.alumno.username}" # Muestra el nombre de usuario del alumno
            f" - "
            f"{self.curso.nombre}"    # Muestra el nombre del curso
        )
