from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from cursos.models import Curso
from .models import Matricula
from django.db.models import Count

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

    # Solo alumnos
    if request.user.tipo != 'alumno':

        messages.error(
            request,
            "Sólo los alumnos pueden matricularse."
        )

        return redirect(
            'detalle_curso',
            curso_id=curso.id
        )

    inscritos = curso.matriculas.count()

    if inscritos >= curso.plazas:

        messages.error(
            request,
            "No quedan plazas."
        )

        return redirect(
            'detalle_curso',
            curso_id=curso.id
        )

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
        curso_id=curso.id
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

# Decorador que asegura que solo los usuarios autenticados puedan acceder a esta vista.
# Si un usuario no ha iniciado sesión, será redirigido a la página de login.
@login_required
def dashboard(request):
    
    # Obtiene el número total de matrículas que tiene el usuario actual.
    # Filtra en la base de datos por el campo 'alumno' usando el usuario de la sesión.
    total_matriculas = (
        Matricula.objects.filter(
            alumno=request.user
        ).count()
    )
    
    # Obtiene la matrícula más reciente realizada por el usuario.
    # Filtra por el usuario actual y usa 'select_related' para traer la información 
    # del curso asociado en una sola consulta a la base de datos (optimización).
    # Ordena por fecha de matrícula de forma descendente (-) y toma el primer resultado (.first()).
    ultima_matricula = (
        Matricula.objects.filter(
            alumno=request.user
        )
        .select_related(
            'curso'
        )
        .order_by(
            '-fecha_matricula'
        )
        .first()
    )
    
    # Obtiene el próximo curso que va a iniciar el usuario, basándose en sus matrículas.
    # Filtra los cursos que tienen matrículas asociadas al usuario actual.
    # Ordena los resultados por la fecha de inicio de forma ascendente para encontrar el más cercano.
    # Toma el primer resultado de la lista.
    proximo_curso = (
        Curso.objects.filter(
            matriculas__alumno=request.user
        )
        .order_by(
            'fecha_inicio'
        )
        .first()
    )
    
    # Renderiza la plantilla HTML especificada y le pasa las variables calculadas
    # en un diccionario (contexto) para que puedan mostrarse en el navegador.
    return render(
        request,
        'matriculas/dashboard.html',
        {
            'total_matriculas': total_matriculas,
            'ultima_matricula': ultima_matricula,
            'proximo_curso': proximo_curso,
        }
    )

# Decorador que restringe el acceso solo a usuarios autenticados.
# Si un usuario anónimo intenta acceder, es enviado al login.
@login_required
def cancelar_matricula(
    request,
    matricula_id
):
    # Busca la matrícula por su clave primaria (pk) y se asegura de que pertenezca al usuario actual.
    # Si la matrícula no existe o pertenece a otro alumno, devuelve un error 404 (No encontrado).
    # Esto es una medida crítica de seguridad para evitar que un usuario borre datos de otro.
    matricula = get_object_or_404(
        Matricula,
        pk=matricula_id,
        alumno=request.user
    )
    
    # Elimina el registro de la matrícula seleccionada de la base de datos.
    matricula.delete()
    
    # Registra un mensaje de éxito en el sistema de mensajes de Django.
    # Este mensaje se mostrará al usuario en la siguiente pantalla que visite.
    messages.success(
        request,
        'Matrícula cancelada.'
    )
    
    # Redirige el navegador del usuario hacia la vista llamada 'mis_cursos'.
    return redirect(
        'mis_cursos'
    )
