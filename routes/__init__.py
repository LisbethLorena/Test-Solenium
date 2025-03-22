from flask import Blueprint

# Importar los Blueprints de cada módulo
from routes.users import users_bp
from routes.meters import meters_bp

# Crear una lista con los Blueprints
blueprints = [users_bp, meters_bp]