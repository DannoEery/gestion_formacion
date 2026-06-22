from django.shortcuts import render, get_object_or_404
# render: permite devolver una plantilla HTML con datos
# get_object_or_404: obtiene un objeto o lanza error 404 si no existe

from .models import Curso
# Importa el modelo Curso desde la app actual


def lista_cursos(request):
    # Vista que muestra la lista de cursos

    cursos = Curso.objects.filter(
        activo=True
    )
    # Obtiene todos los cursos que estén marcados como activos

    return render(
    request,
    'cursos/lista_cursos.html',
    {
        'cursos': cursos,
        'total_cursos': cursos.count()
        # Cuenta el total de cursos activos y lo envía a la plantilla
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