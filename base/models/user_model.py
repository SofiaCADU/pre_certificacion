#Modelo de usuario

#Encapsula toda la logica relacionada con los usuarios en la base de datos.

from base.config.mysqlconnection import connectToMySQL
import re
from flask import flash, redirect, session
from bcrypt import hashpw, gensalt, checkpw

# Exprecion regular para velidar emails
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

class User:
    """
    Esta clase representa a un usuario y sus operaciones dentro de la DB
    """
    db = 'compañero_viaje'

    def __init__(self, data):
        """
        Constructor: Inicializa los atributos del usuario
        """
        self.id = data['id']
        self.nombre = data['nombre']
        self.apellido = data['apellido']
        self.email = data['email']
        self.password = data['password']
        self.created_en = data['created_en']
        self.updated_en = data['updated_en']

    @classmethod
    def guardar_user(cls, data):
        """
        Guarda un nuevo usuario en la base de datos
        """
        # Normaliza nombre y apellido antes de guardar
        data['nombre'] = data['nombre'].capitalize()
        data['apellido'] = data['apellido'].capitalize()
        query = "INSERT INTO users (nombre, apellido, email, password) VALUES (%(nombre)s, %(apellido)s, %(email)s, %(password)s);"
        resultado = connectToMySQL(cls.db).query_db(query, data)
        return resultado  # Devuelve el ID del nuevo usuario
    
    @classmethod
    def obtener_por_email(cls, data):
        """
        Obtiene un usuario por su email
        """
        query = "SELECT * FROM users WHERE email = %(email)s;"
        resultado = connectToMySQL(cls.db).query_db(query, data)
        if not resultado:
            return False
        return cls(resultado[0])
    
    @classmethod
    def obtener_por_id(cls, user_id):
        """
        Obtener un usuario por su ID.
        """
        query = "SELECT * FROM users WHERE id = %(id)s;"
        data = {'id' : user_id}
        resultado = connectToMySQL(cls.db).query_db(query, data)
        if not resultado:
            return None
        return cls(resultado[0])
    
    @staticmethod
    def validar_registro(user):
        is_valid = True
        
        # Validar nombre
        if len(user['nombre']) < 3:
            flash("El nombre debe tener al menos 3 caracteres", 'registro') 
            is_valid = False
        
        # Validar apellido
        if len(user['apellido']) < 3: 
            flash("El apellido debe tener al menos 3 caracteres", 'registro') 
            is_valid = False
        
        # Validar email
        REGEX_EMAIL = re.compile(
            r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        if not REGEX_EMAIL.match(user['email']):
            flash("Dirección de email inválida", 'registro') 
            is_valid = False

        # Validar contraseña
        if len(user['password']) < 8:
            flash("La contraseña debe tener al menos 8 caracteres", 'registro') 
            is_valid = False

        # Validar confirmacion de contraseña
        if user['password'] != user['confirm_password']:
            flash("Las contraseñas no coinciden", 'registro') 
            is_valid = False

        # Verificar si el email ya existe
        user_existente = User.obtener_por_email(
            {'email': user['email']}
        )
        if user_existente:
            flash("El email ya está registrado", 'registro') 
            is_valid = False

        # IMPORTANTE: Retornar el booleano
        return is_valid
    
    @staticmethod
    def validar_login(user):
    # Valida los datos de formulario de inicio de login.
    # Devuelve true su el usuario existe y la contraseña es correcta.

        is_valid = True
        user_in_db = User.obtener_por_email(user)
        if not user_in_db:
            flash("Email no registrado.", 'login')
            is_valid = False
        else:
           if not checkpw(user['password'].encode('utf-8'), user_in_db.password.encode('utf-8')):
                flash("Contraseña incorrecta.", 'login')
                is_valid = False
        return is_valid