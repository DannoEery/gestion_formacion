from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from cursos.models import Curso
from .models import Matricula

# =========================================================================
# VISTA: MATRICULARSE
# =========================================================================
@login_required
def matricularse(request, curso_id):

    curso = get_object_or_404(
        Curso,
        id=curso_id,
        activo=True
    )

    # ==================================
    # 16. SOLO ALUMNOS
    # ==================================

    if request.user.tipo != "alumno":

        messages.error(
            request,
            "Sólo los alumnos pueden matricularse."
        )

        return redirect(
            'detalle_curso',
            curso.id
        )

    # ==================================
    # 14. CONTROL DE PLAZAS
    # ==================================

    inscritos = curso.matriculas.count()

    if inscritos >= curso.plazas:

        messages.error(
            request,
            "No quedan plazas."
        )

        return redirect(
            'detalle_curso',
            curso.id
        )

    # ==================================
    # EVITAR DUPLICADOS
    # ==================================

    matricula, creada = Matricula.objects.get_or_create(
        alumno=request.user,
        curso=curso
    )

    if creada:
        messages.success(
            request,
            "Matrícula realizada correctamente."
        )
    else:
        messages.warning(
            request,
            "Ya estás matriculado en este curso."
        )

    return redirect(
        'detalle_curso',
        curso.id
    )

# =========================================================================
# VISTA: MIS CURSOS
# =========================================================================
@login_required
def mis_cursos(request):
    # Filtra las matrículas para traer solo las que pertenecen al usuario que inició sesión
    # .select_related('curso') hace un SQL JOIN para traer los datos del curso en una sola consulta a la base de datos (Optimización de rendimiento)
    matriculas = Matricula.objects.filter(
        alumno=request.user
    ).select_related('curso')
    
    # Renderiza la plantilla HTML específica pasando el listado de matrículas como contexto
    return render(
        request,
        'matriculas/mis_cursos.html',
        {
            'matriculas': matriculas
        }
    )
