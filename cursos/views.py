from django.shortcuts import render, get_object_or_404

# render: permite devolver una plantilla HTML con datos
# get_object_or_404: obtiene un objeto o lanza error 404 si no existe


from .models import Curso

# Importa el modelo Curso desde la app actual

from profesores.models import Profesor

# Desde el módulo de consultas de Django...
from django.db.models import (
    Q,
)  # ...importa el objeto Q para construir consultas complejas con operadores lógicos (OR / AND).

# Importa las vistas genéricas basadas en clases de Django para realizar operaciones CRUD estándar
from django.views.generic import (
    # Se usa para listar múltiples registros de la base de datos (ej: una lista de cursos)
    ListView,
    # Se usa para mostrar el detalle profundo de un solo registro específico (ej: la ficha de un alumno)
    DetailView,
    # Se usa para renderizar y procesar un formulario que crea un nuevo registro (ej: crear un curso)
    CreateView,
    # Se usa para renderizar y procesar un formulario que edita un registro existente (ej: modificar un curso)
    UpdateView,
    # Se usa para gestionar la confirmación y el proceso de borrado de un registro (ej: eliminar un curso)
    DeleteView,
)

# Importa la versión "perezosa" (lazy) del resolvedor de URLs de Django
from django.urls import reverse_lazy

# Importa el "Mixin" encargado de restringir el acceso a usuarios no autenticados
from django.contrib.auth.mixins import (
    # Es el equivalente en clases al decorador de funciones @login_required
    LoginRequiredMixin
)
# Importa el mixin personalizado que acabamos de crear para el control de accesos
from profesores.mixin import (
    # Esta clase se encargará de validar que el usuario tenga el rol de 'profesor' antes de permitirle ver la vista
    ProfesorMixin
)




# Nueva versión: Define la vista utilizando programación orientada a objetos heredando de ListView
class ListaCursosView(
    # Hereda la clase ListView para reutilizar toda la lógica de listado y paginación de Django
    ListView
):
    # Indica a Django de qué tabla de la base de datos debe extraer los registros de forma automática
    model = Curso

    # Define la ruta exacta de la plantilla HTML que se encargará de renderizar la página
    template_name = "cursos/lista_cursos.html"

    # Renombra la variable que se enviará al HTML para que la recorras como 'cursos' en vez de 'object_list'
    context_object_name = "cursos"

    # Activa la paginación automática dividiendo el listado en grupos de máximo 6 registros por pantalla
    paginate_by = 6

    # Modifica la consulta antes de enviarla a la plantilla
    def get_queryset(self):

        # Obtiene solamente cursos activos
        queryset = Curso.objects.filter(activo=True)

        # Recoge el texto escrito en el buscador
        buscar = self.request.GET.get("buscar", "")

        # Si el usuario escribió algo, filtra
        if buscar:

            queryset = queryset.filter(nombre__icontains=buscar)

        # Devuelve la consulta final
        return queryset


# Vista basada en clases para mostrar el detalle de un curso
class CursoDetailView(DetailView):

    # Modelo que va a buscar Django automáticamente
    model = Curso

    # Plantilla que mostrará los datos
    template_name = "cursos/detalle_curso.html"

    # Nombre de la variable que recibirá el HTML
    context_object_name = "curso"

    # Campo del modelo que usará para buscar
    # En vez de buscar por id, busca por slug
    slug_field = "slug"

    # Nombre del parámetro que viene desde urls.py
    slug_url_kwarg = "slug"

# Vista basada en clases para crear nuevos cursos
# Hereda de CreateView para automatizar la generación, renderizado y validación del formulario de creación
class CursoCreateView(
    LoginRequiredMixin,
    ProfesorMixin,
    CreateView
):

    # Modelo que se va a crear
    # Conecta la vista con el modelo Curso para saber qué tabla debe recibir los datos insertados
    model = Curso

    # Campos que aparecerán automáticamente en el formulario
    # Define la lista exacta de columnas de la base de datos que se transformarán en campos de entrada HTML
    fields = [
        'nombre',
        'descripcion',
        'profesor',
        'fecha_inicio',
        'fecha_fin',
        'plazas',
        'activo',
        'imagen'
    ]

    # Plantilla del formulario
    # Indica el archivo HTML encargado de estructurar y mostrar el formulario en la pantalla del usuario
    template_name = "cursos/curso_form.html"

    # Cuando se cree correctamente vuelve al listado de cursos
    # Utiliza reverse_lazy para posponer la búsqueda de la ruta hasta que el registro se guarde con éxito
    success_url = reverse_lazy(
        "lista_cursos"
    )

# ==========================
# ACTUALIZAR CURSO
# ==========================

# Vista basada en clases para modificar la información de un registro existente
# Hereda de UpdateView, la cual precarga automáticamente los datos del objeto en el formulario usando el ID de la URL
class CursoUpdateView(
    LoginRequiredMixin,
    ProfesorMixin,
    UpdateView
):

    # Modelo que vamos a modificar
    # Vincula la vista con el modelo Curso para saber qué tabla de la base de datos se va a actualizar
    model = Curso

    # Campos que podrá editar el usuario
    # Define de forma explícita las columnas que se le permitirán sobreescribir al usuario (notarás que aquí se omitió 'profesor' e 'imagen')
    fields = [
        'nombre',
        'descripcion',
        'fecha_inicio',
        'fecha_fin',
        'plazas',
        'activo'
    ]

    # Reutilizamos el mismo formulario
    # que usamos para crear
    # Apunta al mismo archivo HTML; Django es lo bastante inteligente como para rellenar los campos en vez de mostrarlos vacíos
    template_name = "cursos/curso_form.html"

    # Después de guardar vuelve al listado
    # Utiliza reverse_lazy para recalcular la ruta de redirección en memoria una vez que los cambios se guarden con éxito
    success_url = reverse_lazy(
        "lista_cursos"
    )

# ==========================
# ELIMINAR CURSO
# ==========================

# Vista basada en clases para borrar un registro de manera definitiva de la base de datos
# Hereda de DeleteView, encargada de verificar la existencia del objeto y gestionar el POST de confirmación
class CursoDeleteView(
    LoginRequiredMixin,
    ProfesorMixin,
    DeleteView):

    # Modelo que vamos a eliminar
    # Conecta la vista con la tabla Curso para indicarle a Django de dónde debe remover el registro
    model = Curso

    # Plantilla de confirmación
    # Define el archivo HTML de seguridad donde se le preguntará al usuario si está seguro de proceder con el borrado
    template_name = "cursos/curso_confirm_delete.html"

    # Después de eliminar vuelve al listado
    # Utiliza reverse_lazy para retrasar la resolución de la URL hasta que la eliminación se ejecute con éxito
    success_url = reverse_lazy(
        "lista_cursos"
    )
