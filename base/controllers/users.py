# base/controllers/user.py

from flask import render_template, request, redirect, session,Blueprint, flash
from base.models.user_model import User
from bcrypt import hashpw, gensalt

bp = Blueprint('user', __name__, url_prefix='/user')

@bp.route('/procesar_registro', methods=['POST'])
def procesar_registro():
    if not User.validar_registro(request.form):
        return redirect('/')
    
    password_hash = hashpw(request.form['password'].encode('utf-8'), gensalt())
    data = {
        **request.form,
        'password': password_hash.decode('utf-8')
    }
    user_id = User.guardar_user(data)
    session['user_id'] = user_id
    flash("¡Registro exitoso!", 'exito')
    return redirect('/viajes')

@bp.route('/procesar_login', methods=['POST'])
def procesar_login():
    if not User.validar_login(request.form):
        return redirect('/')

    user_db = User.obtener_por_email(request.form)
    session['user_id'] = user_db.id
    flash(f"¡Bienvenido de nuevo, {user_db.nombre}!", 'exito')
    return redirect('/viajes')

@bp.route('/logout')
def logout():
    session.clear()
    return redirect('/')