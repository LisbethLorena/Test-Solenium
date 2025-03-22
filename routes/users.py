from flask import Blueprint, request, jsonify
from app import db
from models import User
from sqlalchemy.exc import IntegrityError

users_bp = Blueprint("users", __name__, url_prefix="/users")

# Listar usuarios
@users_bp.route("/",methods=["GET"])
def get_users():
    users = User.query.all()

    if not users: 
        return jsonify({"message": "No hay usuarios registrados", "code": 200})
    return jsonify([{"id": u.id, "name": u.name} for u in users])

# Listar usuario por id
@users_bp.route("/<int:user_id>", methods=["GET"])
def get_user(user_id):
    user = User.query.get(user_id)
    if not user:
        return jsonify({"error": "Usuario no encontrado", "code": 404})
    return jsonify({"id": user.id, "name": user.name})

# Crear usuario
@users_bp.route("/", methods=["POST"])
def create_user():
    data = request.get_json()
    if not data or "id" not in data or "name" not in data:
        return jsonify({"error": "Faltan datos, se esperan id y name", "code": 404})
    
    new_user = User(id=data["id"],name=data["name"])
    try:
        db.session.add(new_user)
        db.session.commit()    
    except IntegrityError as e:
        db.session.rollback()
        error_message = str(e).lower()
        if "foreignkeyviolation" in error_message or "notnullviolation" in error_message:
            return jsonify({"error": "El usuario con este id ya existe", "code": 404})
        return jsonify({"error": f"""Error de integridad en la base de datos, {e}""", "code": 500})
    return jsonify({"message": "Usuario creado", "id": new_user.id, "code": 200})

# Actualizar usuario por id
@users_bp.route("/<int:user_id>", methods=["PUT"])
def update_user(user_id):
    user = User.query.get(user_id)
    if not user:
        return jsonify({"error": "Usuario no encontrado", "code": 404})
    
    data = request.get_json()
    if len(data) == 0:
        return jsonify({"error": "Body vacío", "code": 400})
    if set(data.keys()) != {"name"}:
        return jsonify({"error": "Solo se permite actualizar el parámetro name", "code": 400})
    
    user.name = data.get("name", user.name)    
    db.session.commit()
    return jsonify({"message": "Usuario actualizado", "code": 200})

# Eliminar usuario por id
@users_bp.route("/<int:user_id>", methods=["DELETE"])
def delete_user(user_id):
    user = User.query.get(user_id)
    if not user:
        return jsonify({"error": "Usuario no encontrado", "code": 404})
    
    try:
        db.session.delete(user)
        db.session.commit()
    except IntegrityError as e:
        db.session.rollback()
        error_message = str(e).lower()
        if "foreignkeyviolation" in error_message or "notnullviolation" in error_message:
            return jsonify({"error": "No se puede eliminar el usuario porque tiene medidores asociados", "code": 400})
        return jsonify({"error": f"""Error de integridad en la base de datos, {error_message}""", "code": 500})
    return jsonify({"message": "Usuario eliminado"})
