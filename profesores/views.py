# Importa la función render para generar plantillas HTML con datos de contexto
from django.shortcuts import render
# Importa el modelo Curso para realizar consultas a la base de datos de cursos
from cursos.models import Curso
# Importa el modelo Matricula para gestionar las inscripciones de los estudiantes
from matriculas.models import Matricula
# Importa el decorador personalizado que creamos para restringir el acceso a profesores
from usuarios.decorators import profesor_required


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

    # Renderiza la plantilla HTML enviando las estadísticas calculadas
    return render(
        request,
        'profesores/dashboard.html',
        {
            'total_cursos': total_cursos,
            'total_alumnos': total_alumnos,
        }
    )
