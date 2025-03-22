from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, timezone
from sqlalchemy.sql import func
from sqlalchemy import BigInteger, Integer
db = SQLAlchemy()

class User(db.Model):
    __tablename__ = "tbl_users"  # Nombre de la tabla de los usuarios en la bd

    id = db.Column(Integer, nullable=False, autoincrement=False, primary_key=True) #Llave primaria numero de identidad
    name = db.Column(db.String(150), nullable=False)
    meters = db.relationship("Meter", backref="user", lazy=True) # Relacion 1-N

    def __repr__(self):
        return f"<Usuario {self.name}>"

class Meter(db.Model):
    __tablename__ = "tbl_meters"  # Nombre de la tabla de los medidores en la bd

    serial_number = db.Column(Integer, nullable=False, autoincrement=False, primary_key=True) #Llave primaria numero de serie
    city = db.Column(db.String(100), nullable=False)
    latitude = db.Column(db.Float, nullable=False)
    longitude = db.Column(db.Float, nullable=False)
    fk_user = db.Column(db.Integer, db.ForeignKey("tbl_users.id"), nullable=False)

    def __repr__(self):
        return f"<Medidor {self.serial_number}>"

class Consumption(db.Model):
    __tablename__ = "tbl_consumptions"

    meter_id = db.Column(Integer, db.ForeignKey("tbl_meters.serial_number"), primary_key=True)
    registration_time = db.Column(db.DateTime, primary_key=True, server_default=func.now())  # Fecha automatica
    consumption_kwh = db.Column(db.Float, nullable=False)

    def __repr__(self):
        return f"<Consumo {self.consumption_kwh} kWh con fecha de registro {self.registration_time}>"
