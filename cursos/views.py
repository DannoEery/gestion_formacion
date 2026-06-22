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



def lista_cursos(request):
    # Vista que muestra la lista de cursos

    # Obtener profesor seleccionado
    profesor_id = request.GET.get(
        'profesor'
    )

    # Recoger texto del buscador
    busqueda = request.GET.get(
        "buscar",  # Busca el parámetro llamado 'buscar' dentro de la URL (enviado por el formulario mediante método GET).
        "",  # Define una cadena de texto vacía como valor por defecto si el parámetro 'buscar' no existe en la URL.
    )


    cursos = Curso.objects.filter(
        activo=True
    )
    # Obtiene todos los cursos que estén marcados como activos

    # Filtrar si hay búsqueda
    if busqueda:  # Evalúa si la variable 'busqueda' contiene texto (es decir, si el usuario escribió algo en el buscador).
        cursos = cursos.filter(  # Sobrescribe el QuerySet de 'cursos' aplicando un nuevo filtro a la base de datos.
            Q(nombre__icontains=busqueda)  # Busca si el texto está incluido en el campo 'nombre', ignorando mayúsculas y minúsculas.
            |  # Operador lógico OR (O): el registro se incluirá si cumple la condición de la izquierda O la de la derecha.
            Q(descripcion__icontains=busqueda)  # Busca si el texto está incluido en el campo 'descripcion', también ignorando mayúsculas/minúsculas.
        )
    if profesor_id:  # Evalúa si la variable 'profesor_id' contiene un valor válido (es decir, si no está vacía o es None).
        cursos = cursos.filter(  # Sobrescribe el QuerySet de 'cursos' aplicando un nuevo filtro de base de datos.
            profesor_id=profesor_id  # Restringe los resultados para mostrar únicamente los cursos cuyo campo relacional 'profesor_id' coincida con el ID recibido.
    )
    # Obtener profesores para el formulario
    profesores = Profesor.objects.all()
       
    # ==========================
    # PAGINACION
    # ==========================

    paginator = Paginator(
        cursos,
        6
    )
    # 6 cursos por página


    page_number = request.GET.get(
        'page'
    )
    # Obtiene la página actual


    cursos = paginator.get_page(
        page_number
    )
    # Devuelve solo los cursos de esa página

    

    return render(
    request,
    'cursos/lista_cursos.html',
    {
        'cursos': cursos,
        'total_cursos': paginator.count,
        # Cuenta el total de cursos activos y lo envía a la plantilla
        'busqueda': busqueda,
        'profesores': profesores
    }
)


def detalle_curso(request, slug):

    curso = get_object_or_404(
        Curso,
        slug = slug,
        activo=True
    )


    ocupadas = curso.matriculas.count()


    return render(
        request,
        "cursos/detalle_curso.html",
        {
            "curso": curso,
            "ocupadas": ocupadas
        }
    )