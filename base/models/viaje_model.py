# base/models/viajes_models.py

# Modelo de viaje

from base.config.mysqlconnection import connectToMySQL
from flask import flash, session
from base.models.user_model import User

class Viaje:

    db = "compañero_viaje"

    def __init__(self, data):
        self.id = data['id']
        self.viaje = data['viaje']
        self.destino = data['destino']
        self.descripcion = data['descripcion']
        self.fecha_inicio = data['fecha_inicio']
        self.fecha_fin = data['fecha_fin']
        self.user_id = data['user_id']
        self.creado_en = data['creado_en']
        self.actualizado_en = data['actualizado_en']

        self.autor = None

    @classmethod
    def guardar_viaje(cls,data):
        # Guarda un nuevo viaje en la base de datos.
        query = """
            INSERT INTO viajes (destino, descripcion, fecha_inicio, fecha_fin, autor_id) 
            VALUES (%(destino)s, %(descripcion)s, %(fecha_inicio)s, %(fecha_fin)s, %(autor_id)s);
            """
        resultado = connectToMySQL(cls.db).query_db(query, data)
        return resultado

    @classmethod
    def obtener_por_id(cls, viaje_id):
        query = """
                SELECT v.*, 
                    u.nombre as autor_nombre, u.apellido as autor_apellido
                FROM viajes v
                JOIN users u ON v.autor_id = u.id
                WHERE v.id = %(id)s;
            """
        data = {'id' : viaje_id}
        resultado = connectToMySQL(cls.db).query_db(query, data)
        if not resultado:
            return None
        viaje_data = (resultado[0])
        viaje = cls(viaje_data)

        autor_data = {
                'id': viaje_data['autor_id'],
                'nombre': viaje_data['autor_nombre'],
                'apellido': viaje_data['autor_apellido'],
                'email': None, 
                'password': None,
                'created_en': None,
                'updated_en': None,
            }
        Viaje.autor = User(autor_data)
        return Viaje

    @classmethod
    def obtener_todas(cls):
        query = "SELECT * FROM viajes;"
        resultado = connectToMySQL(cls.db).query_db(query)
        viajes = []
        for row in resultado:
            viaje = (cls(row))

            autor_data = {
                    'id': row['autor_id'],
                    'nombre': row['autor_nombre'],
                    'apellido': row['autor_apellido'],
                    'email': None, 
                    'password': None,
                    'created_en': None,
                    'updated_en': None,
                }
            viaje.autor = User(autor_data)
            viajes.append(viaje)
        return Viaje

    @classmethod
    def obtener_viaje_user(cls, user_id):
        query = "SELECT * FROM viajes WHERE autor_id = %(user_id)s;"
        data = {"user_id" : user_id}
        resultado = connectToMySQL(cls.db).query_db(query, data)
        viajes = []
        for row in resultado:
            viajes.append(cls(row))
        return viajes

    @classmethod
    def actualizar_viaje(cls, data):
        query = """
            UPDATE viajes SET 
                destino = %(destino)s, 
                descripcion = %(descripcion)s, 
                fecha_inicio = %(fecha_inicio)s, 
                fecha_fin = %(fecha_fin)s,
                actualizado_en = NOW() 
            WHERE id = %(id)s;
        """
        resultado = connectToMySQL(cls.db).query_db(query, data)

    @classmethod
    def eliminar_viaje(cls, viaje_id):
        query = "DELETE FROM viajes WHERE id = %(id)s;"
        data = {'id' : viaje_id}
        return connectToMySQL(cls.db).query_db(query, data)

    @staticmethod
    def validar_viaje(form):
        is_valid = True

        if len(form['destino']) < 3:
            flash("El destino debe tener al menos caracteres.", "viaje")
            is_valid = False

        if len(form['descripcion']) < 3:
            flash("La descripcion debe tener al menos 3 caracteres", 'viajes')
            is_valid = False
        
        if not form['fecha_inicio']:
            flash("Se debe ingresar una fecha de inicio.", 'viaje')
            is_valid = False

        if not form['fecha_fin']:
            flash("Se debe ingresar una Fecha de finalizacion.", 'viaje')
            is_valid = False
        
        try:
            from datetime import date
            fecha_inicio = date.fromisoformat(form['fecha_inicio'])
            fecha_fin = date.fromisoformat(form['fecha_fin'])

            if fecha_inicio < date.today():
                flash("La fecha de inicio no puede ser en el pasado.", 'viaje')
                is_valid = False

            if fecha_fin < fecha_inicio:
                flash("La fecha de fin no puede ser anterior a la fecha de inicio.", 'viaje')
                is_valid = False

        except ValueError:
            flash("Formato de fecha invalido.", 'viaje')
            is_valid = False
        
        return is_valid