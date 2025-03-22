from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import os

from models import db, User, Meter
from routes import blueprints

app = Flask(__name__)

# Configuracion de la bd desde las variables de entorno
app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DATABASE_URL")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

# Inicializar la bd
db.init_app(app) #Conecta SQLAlchemy con Flask
migrate = Migrate(app, db) #Habilita migraciones con Flask-Migrate.

# Registrar Blueprints despues de inicializar db
for bp in blueprints:
    app.register_blueprint(bp)

# Ruta de prueba
@app.route("/")
def home():
    return {"message": "API funcionando correctamente"}

if __name__ == "__main__":
    app.run(debug=True)
