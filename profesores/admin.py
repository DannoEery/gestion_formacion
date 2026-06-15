from django.contrib import admin

# Importa el sistema de administración de Django (panel /admin)

from .models import Profesor

# Importa el modelo Profesor desde models.py de la app actual

from django.utils.html import format_html

# Permite generar HTML seguro dentro del admin (en este caso para mostrar imágenes)


@admin.register(Profesor)
# Registra el modelo Profesor en el panel de administración de Django
# Equivale a: admin.site.register(Profesor, ProfesorAdmin)


class ProfesorAdmin(admin.ModelAdmin):
    # Clase que personaliza cómo se muestra el modelo Profesor dentro del admin

    list_display = (
        "miniatura",
        "usuario",
        "especialidad",
        "telefono",
    )
    # Define las columnas que se verán en la lista del admin:
    # - miniatura: muestra la imagen del profesor
    # - usuario: usuario relacionado
    # - especialidad: área del profesor
    # - telefono: contacto

    search_fields = (
        "usuario__username",
        "usuario__first_name",
        "usuario__last_name",
        "especialidad",
    )
    # Permite buscar profesores en el admin por:
    # - nombre de usuario
    # - nombre real
    # - apellidos
    # - especialidad

    list_filter = ("especialidad",)
    # Añade un filtro lateral en el admin para filtrar por especialidad

    ordering = ("usuario__last_name",)
    # Ordena la lista de profesores por el apellido del usuario (A → Z)

    def miniatura(self, obj):
        # Método personalizado para mostrar una imagen en el admin

        if obj.foto:
            # Si el profesor tiene foto, la muestra

            return format_html('<img src="{}" width="50"/>', obj.foto.url)
            # Genera una etiqueta <img> segura con tamaño 50px

        return "-"
        # Si no hay foto, muestra un guion

    miniatura.short_description = "Foto"
    # Nombre de la columna en el admin para este campo personalizado
