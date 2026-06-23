from django.shortcuts import render, get_object_or_404

# render: permite devolver una plantilla HTML con datos
# get_object_or_404: obtiene un objeto o lanza error 404 si no existe

# Desde el módulo de utilidades de paginación nativo de Django...
from django.core.paginator import (
    Paginator,
)  # ...importa la clase encargada de dividir listas de objetos grandes en páginas más pequeñas.


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
    DeleteView
)



# Nueva versión: Define la vista utilizando programación orientada a objetos heredando de ListView
class ListaCursosView(
    # Hereda la clase ListView para reutilizar toda la lógica de listado y paginación de Django
    ListView
):
    # Indica a Django de qué tabla de la base de datos debe extraer los registros de forma automática
    model = Curso
    
    # Define la ruta exacta de la plantilla HTML que se encargará de renderizar la página
    template_name = (
        'cursos/lista_cursos.html'
    )
    
    # Renombra la variable que se enviará al HTML para que la recorras como 'cursos' en vez de 'object_list'
    context_object_name = (
        'cursos'
    )
    
    # Activa la paginación automática dividiendo el listado en grupos de máximo 6 registros por pantalla
    paginate_by = 6

    # Modifica la consulta antes de enviarla a la plantilla
    def get_queryset(self):

        # Obtiene solamente cursos activos
        queryset = Curso.objects.filter(
            activo=True
        )


        # Recoge el texto escrito en el buscador
        buscar = self.request.GET.get(
            "buscar",
            ""
        )


        # Si el usuario escribió algo, filtra
        if buscar:

            queryset = queryset.filter(
                nombre__icontains=buscar
            )


        # Devuelve la consulta final
        return queryset


def detalle_curso(request, slug):

    curso = get_object_or_404(Curso, slug=slug, activo=True)

    ocupadas = curso.matriculas.count()

    return render(
        request, "cursos/detalle_curso.html", {"curso": curso, "ocupadas": ocupadas}
    )
