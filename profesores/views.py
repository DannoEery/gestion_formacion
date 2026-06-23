# Importa la función render para generar plantillas HTML con datos de contexto
from django.shortcuts import render
# Importa el modelo Curso para realizar consultas a la base de datos de cursos
from cursos.models import Curso
# Importa el modelo Matricula para gestionar las inscripciones de los estudiantes
from matriculas.models import Matricula
# Importa el decorador personalizado que creamos para restringir el acceso a profesores
from usuarios.decorators import profesor_required

from django.db.models import Count


# Aplica el decorador para asegurar que solo los profesores accedan a esta vista
@profesor_required
def dashboard_profesor(request):

    # Obtiene el perfil de profesor asociado al usuario que hace la petición
    profesor = request.user.profesor

    # Filtra en la base de datos todos los cursos asignados a este profesor
    cursos = Curso.objects.filter(
        profesor=profesor
    )

    # Cuenta la cantidad total de cursos que tiene este profesor
    total_cursos = cursos.count()

    # Cuenta las matrículas activas en los cursos que dicta este profesor
    total_alumnos = (
        Matricula.objects.filter(
            curso__profesor=profesor
        ).count()
    )


    # Busca el curso más popular del profesor
    # Cuenta cuántas matrículas tiene cada curso
    # Ordena de mayor número de alumnos a menor
    # Selecciona el primero

    curso_popular = (
        Curso.objects.filter(
            profesor=profesor
        )
        .annotate(
            total=Count(
                'matriculas'
            )
        )
        .order_by(
            '-total'
        )
        .first()
    )

    # Renderiza la plantilla HTML enviando las estadísticas calculadas
    return render(
        request,
        'profesores/dashboard.html',
        {
            'total_cursos': total_cursos,
            'total_alumnos': total_alumnos,
        }
    )

# Aplica el decorador para asegurar que solo los profesores accedan a esta vista
@profesor_required
def mis_cursos_profesor(request):

    # Realiza la consulta a la base de datos aplicando un filtro y una optimización
    # Realiza la consulta a la base de datos aplicando un filtro y un cálculo agregado eficiente
    cursos = (
        # Accede al gestor de la base de datos del modelo Curso para iniciar la consulta
        Curso.objects
        # Filtra los registros para traer únicamente los cursos que pertenecen al perfil del profesor actual
        .filter(
            profesor=request.user.profesor
        )
        # Crea un campo virtual temporal llamado 'total_alumnos' que se calcula directamente en la base de datos
        .annotate(
            # Utiliza la función de agregación Count para contar cuántas matrículas están asociadas a cada curso
            total_alumnos=Count(
                'matriculas'
            )
        )
    )
    # Renderiza la plantilla HTML enviando el listado completo de cursos optimizado
    return render(
        request,
        'profesores/mis_cursos.html',
        {
            # Pasa la lista de cursos como contexto para poder iterarla en el HTML
            'cursos': cursos
        }
    )

