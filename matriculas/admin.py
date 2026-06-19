from django.contrib import admin
from .models import Matricula

# Decorador que registra el modelo Matricula con su clase de configuración en el admin de Django
@admin.register(Matricula)
class MatriculaAdmin(admin.ModelAdmin):
    # Columnas que se mostrarán en la tabla de la lista de matrículas
    list_display = (
        'alumno',          # Muestra el alumno (usa el método __str__ del modelo de usuario)
        'curso',           # Muestra el curso (usa el método __str__ del modelo Curso)
        'fecha_matricula', # Muestra la fecha y hora exacta de la inscripción
    )
    
    # Campos por los que se puede buscar en la barra de búsqueda superior
    search_fields = (
        'alumno__username', # Permite buscar por el nombre de usuario del alumno (notación __ para relaciones)
        'curso__nombre',    # Permite buscar por el nombre del curso
    )
    
    
    # Orden predeterminado en el que se mostrarán los registros de la lista
    ordering = (
        '-fecha_matricula', # Ordena de forma descendente (el '-' significa de la más reciente a la más antigua)
    )
