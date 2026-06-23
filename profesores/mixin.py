# Importa el "Mixin" genérico de Django para crear reglas de validación y permisos personalizados
from django.contrib.auth.mixins import UserPassesTestMixin


# Mixin que permite el acceso solamente a profesores
# Hereda de UserPassesTestMixin para obligar a la vista a ejecutar una prueba de seguridad antes de cargar
class ProfesorMixin(UserPassesTestMixin):

    # Esta función decide si el usuario pasa la comprobación
    # Método obligatorio que debe devolver True (da acceso) o False (deniega acceso)
    def test_func(self):

        # Evalúa una condición boicoteando la petición si el tipo de usuario no coincide exactamente
        return (
            # Accede al usuario que hace la petición web y verifica si su atributo 'tipo' es igual a 'profesor'
            self.request.user.tipo == 'profesor'
        )
