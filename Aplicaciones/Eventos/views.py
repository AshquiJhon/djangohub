from django.shortcuts import redirect, render
from .models import Usuario #importando el modelo Usuario
from .models import Evento #importando el modelo Evento
from .models import Participacion
from .models import Notificacion  
from datetime import datetime, time
# Create your views here.
def index(request):
    return render(request,'index.html')
#presentar formulario de Voluntarios en pantalla
def agregarUsuario(request):
    return render(request,'agregarUsuario.html')
#presentar el listado de Voluntarios en pantalla
def listadoUsuarios(request):
    usuariosBdd=Usuario.objects.all()
    return render(request,'listadoUsuarios.html',{'usuarios':usuariosBdd})
def guardarUsuario(request):
    matricula = request.POST['txt_matricula']
    nombre = request.POST['txt_nombre']
    apellido = request.POST['txt_apellido']
    email = request.POST['txt_email']
    tipo_usuario = request.POST['txt_tipo_usuario']

    agregarUsuario = Usuario.objects.create(
        matricula=matricula,
        nombre=nombre,
        apellido=apellido,
        email=email,
        tipo_usuario=tipo_usuario
    )
    return redirect('/listadoUsuarios')
def eliminarUsuario(request,id_usuario):
    usuarioEliminar=Usuario.objects.get(id_usuario=id_usuario)
    usuarioEliminar.delete()
    return redirect('/listadoUsuarios')








def agregarEvento(request):
    return render(request,'agregarEvento.html')

def listadoEventos(request):
    eventosBdd=Evento.objects.all()
    return render(request,'listadoEventos.html',{'eventos':eventosBdd})

def guardarEvento(request):
    titulo = request.POST['txt_titulo']
    descripcion = request.POST['txt_descripcion']
    categoria = request.POST['ddl_categoria']
    fecha = request.POST['txt_fecha']
    hora = request.POST['txt_hora']
    ubicacion = request.POST['txt_ubicacion']
    capacidad = int(request.POST['txt_capacidad'])
    nuevoEvento = Evento.objects.create(
        titulo=titulo,
        descripcion=descripcion,
        categoria=categoria,
        fecha=fecha,
        hora=hora,
        ubicacion=ubicacion,
        capacidad=capacidad,
    )
    return redirect('/listadoEventos')

def editarEvento(request, id_evento):
    eventoEditar =Evento.objects.get(id_evento=id_evento)
    return render(request,"editarEvento.html",{'evento':eventoEditar})

def procesarEdicionEvento(request):
    evento = Evento.objects.get(id_evento=request.POST['id_evento'])
    titulo = request.POST['txt_titulo']
    descripcion = request.POST['txt_descripcion']
    categoria = request.POST['ddl_categoria']
    fecha = request.POST['txt_fecha']
    hora = request.POST['txt_hora']
    ubicacion = request.POST['txt_ubicacion']
    capacidad = request.POST['txt_capacidad']
    # Detectar cambios en la hora o la ubicación
    old_hora = evento.hora
    old_ubicacion = evento.ubicacion
    # Asignar los nuevos valores al objeto evento
    evento.titulo = titulo
    evento.descripcion = descripcion
    evento.categoria = categoria
    evento.fecha = fecha
    evento.hora = hora
    evento.ubicacion = ubicacion
    evento.capacidad = capacidad
    # Guardar el evento editado
    evento.save()
    # Llamar a la función para enviar las notificaciones, pasando tanto old_hora como old_ubicacion
    enviar_notificacion_cambio(evento, old_hora, old_ubicacion)
    return redirect('/listadoEventos/')

def enviar_notificacion_cambio(evento, old_hora, old_ubicacion):
    # Obtener los usuarios registrados en el evento
    participantes = Participacion.objects.filter(evento=evento)
    # Crear una lista de notificaciones solo si hay cambios
    notificaciones = []
    # Asegurarse de que `old_hora` y `evento.hora` son instancias de `datetime.time`
    if isinstance(old_hora, time):  # Comprobamos si es de tipo datetime.time
        old_hora_str = old_hora.strftime('%H:%M')
    else:
        old_hora_str = str(old_hora)

    if isinstance(evento.hora, time):  # Comprobamos si es de tipo datetime.time
        nueva_hora_str = evento.hora.strftime('%H:%M')
    else:
        nueva_hora_str = str(evento.hora)
    # Si la hora ha cambiado (comparar las cadenas de hora en formato 'HH:MM')
    if old_hora_str != nueva_hora_str:
        for participacion in participantes:
            usuario = participacion.usuario
            # Crear una notificación para el cambio de hora
            mensaje = f"La hora del evento '{evento.titulo}' ha cambiado de {old_hora_str} a {nueva_hora_str}."
            notificaciones.append(Notificacion(
                usuario=usuario,
                evento=evento,
                tipo='cambio_horario',
                mensaje=mensaje
            ))
    # Si la ubicación ha cambiado
    if old_ubicacion != evento.ubicacion:
        for participacion in participantes:
            usuario = participacion.usuario
            # Crear una notificación para el cambio de ubicación
            mensaje = f"La ubicación del evento '{evento.titulo}' ha cambiado de '{old_ubicacion}' a '{evento.ubicacion}'."
            notificaciones.append(Notificacion(
                usuario=usuario,
                evento=evento,
                tipo='cambio_ubicacion',
                mensaje=mensaje
            ))
    # Crear notificaciones en la base de datos solo si hay alguna en la lista
    if notificaciones:
        Notificacion.objects.bulk_create(notificaciones)

def listar_notificaciones(request):
    # Obtener todas las notificaciones
    notificaciones = Notificacion.objects.all()
    return render(request, 'listar_notificaciones.html', {'notificaciones': notificaciones})









def agregarParticipacion(request):
    # Obtener todos los datos necesarios
    eventos=Evento.objects.all()
    usuarios=Usuario.objects.all()
    # Renderizar el template con los datos
    return render(request, 'agregarParticipacion.html',{
        'eventos':eventos,
        'usuarios':usuarios
    })
def listadoParticipacion(request):
    participacionesBdd=Participacion.objects.all()
    return render(request,'listadoParticipacion.html',{'participaciones':participacionesBdd})
def guardarParticipacion(request):
    fecha_registro = request.POST['txt_fecha']
    id_usuario = request.POST['ddl_usuario']
    id_evento = request.POST['ddl_evento']

    # Obtener instancias de Usuario y Evento
    usuario = Usuario.objects.get(id_usuario=id_usuario)
    evento = Evento.objects.get(id_evento=id_evento)

    # Crear una nueva participación y guardarla en la base de datos
    nuevaParticipacion = Participacion.objects.create(
        fecha_registro=fecha_registro,
        usuario=usuario,
        evento=evento,
    )
    return redirect('/listadoParticipacion')


