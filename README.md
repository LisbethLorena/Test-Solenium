Gestión de Consumo Energético

Este proyecto es una API desarrollada en Flask con PostgreSQL para gestionar medidores de consumo energético. Se puede ejecutar tanto localmente como en Docker.

1. Requisitos
🔹 Python 3.10+
🔹 PostgreSQL
🔹 Docker y Docker Compose
🔹 Postman (opcional, para pruebas)

2. Configuración Local
🔹 1. Clonar el repositorio
    -- git clone <URL_DEL_REPOSITORIO>
    -- cd <NOMBRE_DEL_PROYECTO>
🔹 2. Crear un entorno virtual e instalar dependencias
    -- python -m venv venv
    -- venv\Scripts\activate
    -- pip install -r requirements.txt
🔹 3. Configurar variables de entorno
    Crea un archivo .env en la raíz con completar como es debido:
    DATABASE_URL=postgresql://usuario:password@localhost/nombre_base_datos
🔹 4. Crear la base de datos y aplicar migraciones
    -- flask db upgrade
🔹 5. Ejecutar la API
    -- flask run
    La API estará disponible en: http://127.0.0.1:5000/

3. Configuración con Docker
🔹 1. Contenedores
    -- docker-compose up --build
🔹 2. Verificar contenedor
    -- docker exec -it postgres_db psql -U user_test -d test_solenium
    Enlistar las tablas o esquemas
    -- \dt
🔹 3. Acceder a la API
    http://127.0.0.1:5000/

4. Pruebas con Postman
    Puedes importar la colección de Postman y configurar la variable base_url:
        http://127.0.0.1:5000

5. Endpoints Principales
🔹 Gestion usuarios
    GET /users/ → Obtener todos los usuarios
    POST /users/ → Crear un usuario
    PUT /users/<id> → Actualizar usuario
    DELETE /users/<id> → Eliminar usuario

🔹 Gestion medidores
    GET /meters/ → Obtener todos los medidores
    POST /meters/sign → Registrar un medidor
    POST /meters/<serial_number>/generate_consumption → Generar consumo ficticio
    GET /meters/<serial_number>/consumption_history → Ver historial de consumo
    PUT /meters/<serial_number> → Actualizar medidor
    DELETE /meters/<serial_number> → Eliminar medidor

6. Detener los contenedores de Docker
    -- docker-compose down
