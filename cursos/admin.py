from django.contrib import admin
from datetime import datetime, time, timedelta
from django.utils import timezone
from django.utils.html import format_html
from .models import Curso

# 🔍 Filtro temporal personalizado
# Se hereda de SimpleListFilter para crear una barra de filtrado lateral propia en el panel de administración
class FiltroFechas(admin.SimpleListFilter):
    # 'title' es el texto visible que encabezará el bloque de este filtro en la interfaz lateral
    title = 'Filtro temporal' 
    # 'parameter_name' es el nombre que tomará la variable en la URL del navegador (ej: ?periodo=hoy)
    parameter_name = 'periodo' 

    # Define las opciones clicables que el usuario verá en el panel lateral de administración
    def lookups(self, request, model_admin):
        # Lista base con opciones fijas y predefinidas de tiempo relativo
        base = [
            ('hoy', 'Hoy'),
            ('manana', 'Mañana'),
            ('semana', 'Esta semana'),
            ('mes', 'Este mes'),
        ]
        
        # Obtiene la fecha actual del servidor ajustada a la zona horaria configurada en Django
        hoy = timezone.localdate()
        year = hoy.year
        month = hoy.month
        
        # 👉 Mes actual + 11 siguientes
        # Bucle para generar dinámicamente los próximos 12 meses en el filtro, empezando por el actual
        for i in range(12):
            total_month = month + i
            # Controla el cambio de año cuando la suma de meses supera 12 (Diciembre)
            y = year + (total_month - 1) // 12
            # Calcula el número de mes correcto (del 1 al 12) usando el operador residuo %
            m = (total_month - 1) % 12 + 1
            
            # Genera un identificador único para la URL, por ejemplo: 'm_2026_6'
            value = f'm_{y}_{m}' 
            # Genera el texto visible formateado con el nombre del mes completo y el año (ej: "junio 2026")
            label = datetime(y, m, 1).strftime('%B %Y')
            # Añade la opción dinámica a la lista de opciones del filtro
            base.append((value, label))
            
        return base

    # Modifica la consulta a la base de datos (QuerySet) según la opción que el usuario haya pulsado
    def queryset(self, request, queryset):
        hoy = timezone.localdate()
        
        # 📅 HOY
        # Si el usuario pulsa "Hoy", filtra los registros cuya 'fecha_inicio' esté entre las 00:00:00 y las 23:59:59 del día actual
        if self.value() == 'hoy':
            inicio = datetime.combine(hoy, time.min)
            fin = datetime.combine(hoy, time.max)
            return queryset.filter(fecha_inicio__range=(inicio, fin))
            
        # 📅 MAÑANA
        # Calcula el día siguiente y filtra de forma idéntica, cubriendo todo el rango horario de ese día
        if self.value() == 'manana':
            d = hoy + timedelta(days=1)
            inicio = datetime.combine(d, time.min)
            fin = datetime.combine(d, time.max)
            return queryset.filter(fecha_inicio__range=(inicio, fin))
            
        # 📅 ESTA SEMANA
        # Localiza el primer día de la semana actual (lunes = 0) y calcula el rango hasta el domingo finalizando a última hora
        if self.value() == 'semana':
            inicio_d = hoy - timedelta(days=hoy.weekday())
            fin_d = inicio_d + timedelta(days=6)
            inicio = datetime.combine(inicio_d, time.min)
            fin = datetime.combine(fin_d, time.max)
            return queryset.filter(fecha_inicio__range=(inicio, fin))
            
        # 📅 ESTE MES
        # Encuentra el primer día del mes actual y el primer día del mes siguiente para hacer un filtro de "mayor o igual que" y "menor que"
        if self.value() == 'mes':
            inicio_d = hoy.replace(day=1)
            # Evita errores de desbordamiento en diciembre saltando al año siguiente
            if hoy.month == 12:
                fin_d = hoy.replace(year=hoy.year + 1, month=1, day=1)
            else:
                fin_d = hoy.replace(month=hoy.month + 1, day=1)
            return queryset.filter(fecha_inicio__gte=inicio_d, fecha_inicio__lt=fin_d)
            
        # 📅 MES SELECCIONADO
        # Si el valor de la URL empieza por 'm_', significa que se seleccionó uno de los 12 meses dinámicos
        if self.value() and self.value().startswith('m_'):
            # Descompone la cadena de texto (ej: 'm_2026_6') para extraer las variables numéricas de año y mes
            _, year, month = self.value().split('_')
            year = int(year)
            month = int(month)
            
            # Establece el inicio el día 1 de ese mes
            inicio = datetime(year, month, 1)
            # Calcula el límite superior del filtro (el día 1 del mes siguiente)
            if month == 12:
                fin = datetime(year + 1, 1, 1)
            else:
                fin = datetime(year, month + 1, 1)
            return queryset.filter(fecha_inicio__gte=inicio, fecha_inicio__lt=fin)
            
        # Si no se selecciona ningún filtro, devuelve todos los registros originales sin alterar
        return queryset

# Registra el modelo 'Curso' en el panel de administración vinculándolo a las reglas de la clase 'CursoAdmin'
@admin.register(Curso)
class CursoAdmin(admin.ModelAdmin):
    # Columnas que se mostrarán ordenadas en forma de tabla en la vista de lista general
    list_display = ('miniatura', 'nombre', 'profesor', 'fecha_inicio', 'fecha_fin', 'activo',)
    
    # Habilita una barra de búsqueda superior que busca coincidencias de texto en estos campos específicos.
    # Los dos últimos usan '__' para acceder a atributos del modelo relacionado (Relación ForeignKey del Profesor)
    search_fields = ('nombre', 'descripcion', 'profesor__usuario__first_name', 'profesor__usuario__last_name',)
    
    # Agrega los bloques de filtros en el lateral derecho: el campo booleano 'activo' y el filtro personalizado temporal
    list_filter = ('activo', FiltroFechas,)
    
    # Define el criterio de ordenación por defecto de las filas (alfabéticamente por el nombre del curso)
    ordering = ('nombre',)
    
    # Genera automáticamente el slug desde el nombre
    prepopulated_fields = {
        'slug': (
            'nombre',
        )
    }
    
    # Estructura y agrupa los campos del formulario de edición/creación en secciones visuales (cajas con títulos)
    fieldsets = (
        ('Información General', {
            'fields': ('nombre', 'descripcion', 'profesor', 'slug' )
        }),
        ('Planificación', {
            'fields': ('fecha_inicio', 'fecha_fin', 'plazas', )
        }),
        ('Publicación', {
            'fields': ('activo', 'imagen', )
        }),
    )

    # Método personalizado para renderizar la imagen del curso directamente en la tabla de registros
    def miniatura(self, obj):
        # Comprueba si el objeto actual tiene un archivo de imagen subido
        if obj.imagen:
            # Renderiza código HTML seguro para incrustar la imagen fijando un ancho de 80 píxeles
            return format_html('<img src="{}" width="80" />', obj.imagen.url)
        # Si no hay imagen, muestra un guion como texto alternativo
        return '-'
        
    # Cambia el título de la columna en la tabla del panel de administración (por defecto usaría el nombre del método)
    miniatura.short_description = 'Imagen'
