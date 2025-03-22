from flask import Blueprint, request, jsonify
from app import db
from models import Meter, User, Consumption
from sqlalchemy.exc import IntegrityError
import requests
import random
from datetime import datetime, timezone

# Función para obtener latitud y longitud desde Open-Meteo
def get_coordinates(city):
    url = f"https://geocoding-api.open-meteo.com/v1/search?name={city}&count=1&language=es&format=json"
    
    try:
        response = requests.get(url, timeout=5)
        response.raise_for_status()
        data = response.json()
        # print("Data coordenadas---->",data)
        if "results" in data and len(data["results"]) > 0:
            if data["results"][0]["country"] == "Colombia":
                return data["results"][0]["latitude"], data["results"][0]["longitude"]
            return None, None
        return None, None
    except requests.exceptions.RequestException as e:
        print(f"Error al obtener coordenadas: {e}")
        return None, None
    
meters_bp = Blueprint("meters", __name__, url_prefix="/meters")

# Listar medidores
@meters_bp.route("/", methods=["GET"])
def get_meters():
    meters = Meter.query.all()
    if not meters: 
        return jsonify({"message": "No hay medidores registrados", "code": 200})    
    return jsonify([
        {"serial_number": m.serial_number, "city": m.city, "id_user": m.fk_user}
        for m in meters
    ])

# Listar medidor por numero de serie
@meters_bp.route("/<int:serial_number>", methods=["GET"])
def get_meter(serial_number):
    meter = Meter.query.get(serial_number)
    if not meter:
        return jsonify({"error": "Medidor no encontrado","code": 404})
    return jsonify({
        "serial_number": meter.serial_number,
        "city": meter.city,
        "latitude": meter.latitude,
        "longitude": meter.longitude,
        "id_user": meter.fk_user
    })

# Crear medidor
@meters_bp.route("/sign", methods=["POST"])
def create_meter():
    data = request.get_json()
    if not data or "serial_number" not in data or "city" not in data or "user_id" not in data:
        return jsonify({"error": "Faltan datos, se esperan serial_number, city, user_id", "code": 404})
    
    user = User.query.get(data["user_id"])
    if not user:
        return jsonify({"error": "Usuario no registrado", "code": 404})
    
    latitude, longitude = get_coordinates(data["city"])
    if latitude is None or longitude is None:
        return jsonify({"error": "No se pudo obtener la ubicación de la ciudad o no está en Colombia", "code": 404})
    
    new_meter = Meter(
        serial_number = data["serial_number"],
        city = data["city"],
        latitude = latitude,
        longitude = longitude,
        fk_user = data["user_id"]
    )    
    try:
        db.session.add(new_meter)
        db.session.commit()
    except IntegrityError:
        db.session.rollback()
        return jsonify({"error": "El medidor con este número de serie ya existe", "code": 404})    
    return jsonify({"message": "Medidor creado", "id": new_meter.serial_number, "code": 200})

# Actualizar medidor por número de serie
@meters_bp.route("/<int:serial_number>", methods=["PUT"])
def update_meter(serial_number):
    meter = Meter.query.get(serial_number)
    if not meter:
        return jsonify({"error": "Medidor no encontrado", "code": 404})
    
    data = request.get_json()
    if len(data) == 0:
        return jsonify({"error": "Body vacío", "code": 400})
    if set(data.keys()) != {"city", "id_user"}:
        return jsonify({"error": "Solo se permite actualizar los parámetros city e id_user", "code": 400})

    # Si la ciudad cambia, obtener nueva latitud y longitud
    if data["city"] != meter.city:
        lat, lon = get_coordinates(data["city"])
        if lat is None or lon is None:
            return jsonify({"error": "No se pudo obtener la ubicación de la ciudad o no está en Colombia", "code": 400})
        meter.latitude = lat
        meter.longitude = lon

    meter.city = data.get("city", meter.city)
    meter.fk_user = data.get("id_user", meter.fk_user)
    
    db.session.commit()
    return jsonify({"message": "Medidor actualizado", "code": 200})

# Eliminar medidor
@meters_bp.route("/<int:serial_number>", methods=["DELETE"])
def delete_meter(serial_number):
    meter = Meter.query.get(serial_number)
    if not meter:
        return jsonify({"error": "Medidor no encontrado", "code": 404})
    
    db.session.delete(meter)
    db.session.commit()
    return jsonify({"message": "Medidor eliminado"})

# Endpoint para generar consumo en un medidor
@meters_bp.route("/<int:serial_number>/generate_consumption", methods=["POST"])
def generate_consumption(serial_number):
    meter = Meter.query.get(serial_number)
    if not meter:
        return jsonify({"error": "Medidor no encontrado", "code": 404})

    consumption_value = round(random.uniform(0.1, 10.0), 2)
    date_now = datetime.now(timezone.utc)

    new_consumption = Consumption(
        meter_id = meter.serial_number,
        registration_time = date_now,
        consumption_kwh = consumption_value
    )

    db.session.add(new_consumption)
    db.session.commit()
    return jsonify({
        "message": "Consumo generado",
        "serial_nummber": meter.serial_number,
        "consumption_kwh": consumption_value,
        "registration_time": date_now.strftime("%Y-%m-%d %H:%M:%S"),
        "code": 200
    })

# Endpoint para consultar el historial de consumo por medidor
@meters_bp.route("/<int:serial_number>/consumption_history", methods=["GET"])
def get_consumption_history(serial_number):
    meter = Meter.query.get(serial_number)
    if not meter:
        return jsonify({"error": "Medidor no encontrado", "code": 404})

    consumptions = Consumption.query.filter_by(meter_id=meter.serial_number).order_by(Consumption.registration_time.desc()).all()
    if not consumptions:
        return jsonify({"message": "No hay registros de consumo para este medidor", "code": 200})

    return jsonify(
    {
        "meter_id": meter.serial_number,
        "history": [{
            "consumption_kwh": dato.consumption_kwh,
            "registration_time": dato.registration_time.strftime("%Y-%m-%d %H:%M:%S")
        }for dato in consumptions],
        "code": 200
    })