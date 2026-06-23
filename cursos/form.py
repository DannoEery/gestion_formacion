# Importa el módulo de formularios nativo de Django para gestionar la entrada de datos
from django import forms

# Importa el modelo Curso para vincularlo directamente con la estructura del formulario
from .models import Curso


# Define una clase de formulario que mapea de forma automática un modelo de la base de datos
class CursoForm(
    # Hereda de ModelForm, lo que automatiza la creación de inputs HTML basados en las columnas del modelo
    forms.ModelForm
):
    # Clase interna de configuración encargada de definir el comportamiento y origen del formulario
    class Meta:
        # Indica a Django que este formulario debe construirse utilizando la estructura del modelo Curso
        model = Curso

        # Mapea e incluye absolutamente todas las columnas (campos) del modelo como campos de entrada en el HTML
        fields = "__all__"

        # Diccionario de configuración para personalizar el renderizado y atributos HTML de cada campo
        widgets = {
            # Selecciona el campo 'nombre' del modelo para modificar su comportamiento visual
            "nombre": forms.TextInput(
                # Especifica que se debe renderizar como un input de texto tradicional (<input type="text">)
                attrs={
                    # Inyecta atributos directamente dentro de la etiqueta HTML generada por Django
                    "class":
                    # Aplica la clase CSS de Bootstrap para que el campo tenga bordes limpios y ocupe el 100% del ancho
                    "form-control"
                }
            ),
        }
