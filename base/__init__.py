from flask import Flask, render_template
from datetime import datetime
from base.controllers.users import bp as users_bp
from base.controllers.viajes import bp as viajes_bp

def format_date(value, format='%d/%m/%Y'):
    """Convierte una cadena de fechas en un onjeto datetime y lo formatea. Para que se muestre como yo lo necesito."""
    if isinstance(value, str):
        value = datetime.strptime(value, '%Y-%m-%d')
    return value.strftime(format)

def create_app():
    app = Flask(__name__)
    app.config.from_mapping(
        SECRET_KEY='dev',
        DEBUG=True,
    )
    
    app.register_blueprint(users_bp)
    app.register_blueprint(viajes_bp)

    app.add_template_filter(format_date)

    @app.route('/')
    def index():
        return render_template('auth.html')
    return app