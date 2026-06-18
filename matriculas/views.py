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
    # Busca el curso por su ID. Si no existe o no está activo, devuelve un error 404 de inmediato
    curso = get_object_or_404(Curso, pk=curso_id, activo=True)

    # Intenta obtener la matrícula. Si no existe, la crea en la base de datos automáticamente.
    # 'matricula' contiene el objeto y 'creada' es un booleano (True si se creó, False si ya existía)
    matricula, creada = Matricula.objects.get_or_create(
        alumno=request.user,  # Asigna al usuario que tiene la sesión iniciada
        curso=curso,          # Asigna el curso encontrado arriba
    )

    # Envía una alerta de éxito si el registro es nuevo en la base de datos
    if creada:
        messages.success(request, "Matrícula realizada correctamente.")
    # Envía una alerta de advertencia si el usuario ya estaba inscrito previamente
    else:
        messages.warning(request, "Ya estás matriculado en este curso.")

    # Redirige al usuario de vuelta a la página de detalles de ese mismo curso
    return redirect("detalle_curso", curso.id)


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
