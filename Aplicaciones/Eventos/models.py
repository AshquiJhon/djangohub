from django.db import models

# Creación de la tabla Usuario
class Usuario(models.Model):
    id_usuario = models.AutoField(primary_key=True)
    matricula = models.CharField(max_length=50, unique=True)
    nombre = models.CharField(max_length=100)
    apellido = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    tipo_usuario = models.CharField(
        max_length=15,
        choices=[('estudiante', 'Estudiante'), ('administrador', 'Administrador')],
        default='estudiante'
    )
    
    def __str__(self):
        return f"{self.nombre} {self.apellido} ({self.tipo_usuario})"


# Creación de la tabla Evento
class Evento(models.Model):
    id_evento = models.AutoField(primary_key=True)
    titulo = models.CharField(max_length=150)
    descripcion = models.TextField()
    categoria = models.CharField(
        max_length=15,
        choices=[('recreativo', 'Recreativo'), ('cultural', 'Cultural'), ('deportivo', 'Deportivo')]
    )
    fecha = models.DateField()
    hora = models.TimeField()
    ubicacion = models.CharField(max_length=200)
    capacidad = models.PositiveIntegerField()

    def __str__(self):
        return f"{self.titulo} ({self.categoria})"



# Creación de la tabla Participacion
class Participacion(models.Model):
    id_participacion = models.AutoField(primary_key=True)
    fecha_registro = models.DateTimeField(auto_now_add=True)
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    evento = models.ForeignKey(Evento, on_delete=models.CASCADE)
    
    def __str__(self):
        return f"Participación: {self.usuario.nombre} {self.usuario.apellido} en {self.evento.titulo}"


# Creación de la tabla Notificacion
class Notificacion(models.Model):
    id_notificacion = models.AutoField(primary_key=True)
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    evento = models.ForeignKey(Evento, on_delete=models.CASCADE, null=True, blank=True)
    tipo = models.CharField(
        max_length=20,
        choices=[('cambio_horario', 'Cambio de Horario'), ('cambio_ubicacion', 'Cambio de Ubicación'), ('recordatorio', 'Recordatorio')]
    )
    mensaje = models.TextField()
    fecha_envio = models.DateTimeField(auto_now_add=True)
    leida = models.BooleanField(default=False)
    
    def __str__(self):
        return f"Notificación para {self.usuario.nombre}: {self.tipo}"
