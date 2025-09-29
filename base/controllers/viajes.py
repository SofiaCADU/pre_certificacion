from base.models.viaje_model import Viaje
from base.models.user_model import User
from flask import render_template, redirect, request, session, Blueprint, flash

bp = Blueprint('viajes', __name__, url_prefix = '/viajes')

# Controlador de viajes

bp = Blueprint('viajes', __name__, url_prefix = '/viajes')

# Ruta Dashboard
@bp.route('/')
def dashboard():
    if 'user_id' not in session:
        return redirect('/')
    viajes = Viaje.obtener_todas() # Obtiene todos los viajes con su autor
    user_actual = User.obtener_por_id(session['user_id']) # Ayuda a obtener la informacion del usuario que esta en la sesion

    return render_template('dashboard.html', viajes=viajes, user=user_actual)


@bp.route("/agregar", methods=['POST'])
def agregar_viaje():
    if 'user_id' not in session:
        return redirect('/')
    
    if not Viaje.validar_viaje(request.form): # Validar los datos
        return redirect('/viajes')
    
    data = {  # Se cre el diccionario de datos
        'destino': request.form['destino'],
        'descripcion': request.form['descripcion'],
        'fecha_inicio': request.form['fecha_inicio'],
        'fecha_fin': request.form['fecha_fin'],
        'autor_id': session['user_id']
    }
    Viaje.guardar_viaje(data) # Con esto se guardara el viaje 
    flash("¡Viaje agregado con éxito!", 'exito')
    return redirect('/viajes')

# Ruta para editar la pagina
@bp.route('/editar/<int:id>')
def pagina_editar(id):
    if 'user_id' not in session:
        return redirect('/')
    viaje  = Viaje.obtener_por_id(id)

    if not viaje or viaje.autor_id != session['user_id']:
        flash("No tienes permiso para editar este viaje.", 'error')
        return redirect('/viajes')
    
    viaje.fecha_inicio_str = viaje.fecha_inicio.strftime('%Y-%m-%d')
    viaje.fecha_fin_str = viaje.fecha_fin.strftime('%Y-%m-%d')

    return render_template('editar_viajes.html', viaje=viaje)

# Ruta para procesar lo que se edito
@bp.route('/procesar_editar', methods=['POST'])
def procesar_editar():
    if 'user_id' not in session:
        return redirect('/')
    viaje_a_editar = Viaje.obtener_por_id(request.form['id'])

    if not viaje_a_editar or viaje_a_editar.autor_id != session['user_id']:
        flash("No tienes permisos para editar este viaje.", 'error')
        return redirect('/viajes')
    
    if not Viaje.validar_viaje(request.form):
        return redirect(f"/viajes/editar/{request.form['id']}")
    
    Viaje.actualizar_viaje(request.form)
    flash("¡Viaje actualizado con éxito!", 'exito')
    return redirect('/viajes')

# Ruta para borrar el viaje
@bp.route('/borrar/<int:id>')
def  borrar_viaje(id):
    if 'user_id' not in session:
        return redirect('/')
    viaje_a_borrar = Viaje.obtener_por_id(id)

    if not viaje_a_borrar or viaje_a_borrar.autor.id != session['user_id']:
        flash("No tienes permiso para borrar este viaje.", 'error')
        return redirect('/viajes')
    Viaje.eliminar_viaje(id)
    flash("¡El viaje a sido borrado con éxito!", 'exito')
    return redirect('/visitas')

@bp.route('/calendario')
def calendario():
    if 'user_id' not in session:
        return redirect('/')
    
    user = User.obtener_por_id(session['user_id'])
    viajes_user = Viaje.obtener_viaje_user(session['user_id'])

    return render_template('calendario.html', user=user, viajes=viajes_user)

