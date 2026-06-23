from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from cursos.models import Curso
from .models import Matricula
from django.db.models import Count
from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin

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


    if request.user.tipo != "alumno":

        messages.error(
            request,
            "Sólo los alumnos pueden matricularse."
        )

        return redirect(
            "detalle_curso",
            slug=curso.slug
        )


    inscritos = curso.matriculas.count()


    if inscritos >= curso.plazas:

        messages.error(
            request,
            "No quedan plazas."
        )

        return redirect(
            "detalle_curso",
            slug=curso.slug
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
        "detalle_curso",
        slug=curso.slug
    )

# =========================================================================
# VISTA: MIS CURSOS
# =========================================================================
@login_required
def mis_cursos(request):

    matriculas = Matricula.objects.filter(alumno=request.user).select_related(
        "curso", "curso__profesor", "curso__profesor__usuario"
    )

    return render(request, "matriculas/mis_cursos.html", {"matriculas": matriculas})


# Define la vista para el panel de control del estudiante usando programación orientada a objetos
class DashboardAlumnoView(
    # PRIMER FILTRO DE SEGURIDAD: Obliga a que el usuario haya iniciado sesión antes de poder continuar
    LoginRequiredMixin,
    # TIPO DE VISTA: Hereda de TemplateView, ideal para páginas estáticas o paneles que solo muestran datos sin procesar formularios
    TemplateView
):
    # Indica de forma explícita la ruta de la plantilla HTML que se encargará de pintar la interfaz del alumno
    template_name = (
        'matriculas/dashboard.html'
    )
    
    # Método encargado de recolectar y enviar variables dinámicas (contexto) hacia el archivo HTML
    def get_context_data(
        self,
        **kwargs
    ):
        # Ejecuta el método original de la clase padre para heredar el diccionario de contexto base de Django
        context = super().get_context_data(
            **kwargs
        )
        
        # Inyecta una nueva variable llamada 'total_matriculas' dentro del diccionario para enviarla al HTML
        context[
            'total_matriculas'
        ] = (
            # Accede al modelo Matricula y filtra los registros en la base de datos
            Matricula.objects.filter(
                # Busca únicamente las inscripciones asociadas al alumno (usuario que hace la petición)
                alumno=self.request.user
            # Cuenta el número total de filas encontradas para este estudiante específico
            ).count()
        )
        
        # Devuelve el diccionario de datos ya actualizado y listo para que la plantilla lo renderice
        return context



# Decorador que restringe el acceso solo a usuarios autenticados.
# Si un usuario anónimo intenta acceder, es enviado al login.
@login_required
def cancelar_matricula(request, matricula_id):
    # Busca la matrícula por su clave primaria (pk) y se asegura de que pertenezca al usuario actual.
    # Si la matrícula no existe o pertenece a otro alumno, devuelve un error 404 (No encontrado).
    # Esto es una medida crítica de seguridad para evitar que un usuario borre datos de otro.
    matricula = get_object_or_404(Matricula, pk=matricula_id, alumno=request.user)

    # Elimina el registro de la matrícula seleccionada de la base de datos.
    matricula.delete()

    # Registra un mensaje de éxito en el sistema de mensajes de Django.
    # Este mensaje se mostrará al usuario en la siguiente pantalla que visite.
    messages.success(request, "Matrícula cancelada.")

    # Redirige el navegador del usuario hacia la vista llamada 'mis_cursos'.
    return redirect("mis_cursos")
