from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from cursos.models import Curso
from .models import Matricula
from django.db.models import Count
from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils import timezone 

from .models import Matricula


# =========================================================================
# VISTA: MATRICULARSE
# =========================================================================
@login_required
def matricularse(request, curso_id):

    curso = get_object_or_404(Curso, id=curso_id, activo=True)

    if request.user.tipo != "alumno":

        messages.error(request, "Sólo los alumnos pueden matricularse.")

        return redirect("detalle_curso", slug=curso.slug)

    inscritos = curso.matriculas.count()

    if inscritos >= curso.plazas:

        messages.error(request, "No quedan plazas.")

        return redirect("detalle_curso", slug=curso.slug)

    matricula, creada = Matricula.objects.get_or_create(
        alumno=request.user, curso=curso
    )

    if creada:
        messages.success(request, "Matrícula realizada correctamente.")
    else:
        messages.warning(request, "Ya estás matriculado en este curso.")

    return redirect("detalle_curso", slug=curso.slug)


# =========================================================================
# VISTA: MIS CURSOS
# =========================================================================
@login_required
def mis_cursos(request):

    matriculas = Matricula.objects.filter(alumno=request.user).select_related(
        "curso", "curso__profesor", "curso__profesor__usuario"
    )

    return render(request, "matriculas/mis_cursos.html", {"matriculas": matriculas})


# Dashboard del alumno usando TemplateView
class DashboardAlumnoView(LoginRequiredMixin, TemplateView):

    template_name = "matriculas/dashboard.html"

    def get_context_data(self, **kwargs):

        context = super().get_context_data(**kwargs)

        # Matrículas del alumno actual
        matriculas = Matricula.objects.filter(alumno=self.request.user).select_related(
            "curso"
        )

        # Total de cursos matriculados
        context["total_matriculas"] = matriculas.count()

        # Última matrícula
        context["ultima_matricula"] = matriculas.order_by("-fecha_matricula").first()

        # Últimas matrículas
        context["ultimas_matriculas"] = matriculas.order_by("-fecha_matricula")[:5]

        # Próximo curso por fecha de inicio
        context["proximo_curso"] = (
            matriculas.filter(curso__fecha_inicio__gte=timezone.now().date())
            .order_by("curso__fecha_inicio")
            .first()
        )

        # Cursos disponibles activos
        context["cursos_disponibles"] = Curso.objects.filter(activo=True).count()

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
