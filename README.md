# SuperFix API

API backend para SuperFix, una plataforma de servicios y profesionales, desarrollada en **Python** usando **Flask**, **MongoDB** y **SocketIO** para comunicación en tiempo real.

## Características principales

- **Usuarios:** Registro, consulta y actualización de usuarios.
- **Posts:** Publicación y búsqueda geolocalizada de servicios.
- **Chats:** Mensajería en tiempo real entre usuarios.
- **Favoritos:** Guardar y eliminar posts favoritos.
- **Rubros:** Gestión de categorías/rubros de servicios.
- **Subida de archivos:** Fotos y PDFs a AWS S3.
- **Autenticación:** Verificación de token Firebase en cada request.
- **WebSockets:** Notificaciones y chats en vivo con Flask-SocketIO.

## Estructura del proyecto

```
src/
├── app.py                # Archivo principal de la API
├── config.py             # Configuración general
├── extensions.py         # Inicialización de extensiones (SocketIO)
├── db/
│   ├── connect.py        # Conexión a MongoDB
│   └── test_mongo.py     # Prueba de conexión
├── models/               # Modelos de datos (User, Post, Chat, etc.)
├── routes/               # Rutas de la API (users, posts, chats, etc.)
```

## Requisitos

- Python 3.11+
- MongoDB (local o Atlas)
- AWS S3 (para subida de archivos)
- Firebase (para autenticación)
- Dependencias principales:
  - Flask
  - Flask-SocketIO
  - pymongo
  - boto3
  - firebase-admin
  - eventlet

## Instalación

1. Clona el repositorio:
   ```bash
   git clone https://github.com/tuusuario/superfix-backend.git
   cd superfix-backend/src
   ```

2. Instala las dependencias:
   ```bash
   pip install -r requirements.txt
   ```

3. Configura las credenciales de Firebase y AWS S3 en `src/nube-560f3-firebase-adminsdk-fbsvc-96d6ca292a.json` y variables de entorno.

4. Inicia MongoDB localmente o configura la conexión en `db/connect.py`.

## Ejecución

```bash
python app.py
```
El servidor se inicia en `http://localhost:5000`.

## Endpoints principales

- `/api/users` - Usuarios
- `/api/post` - Posts y búsqueda geolocalizada
- `/api/chats` - Chats y mensajes
- `/api/favorites` - Favoritos
- `/api/rubs` - Rubros
- `/api/upload` - Subida de archivos

## WebSockets

- Evento `join_user` para notificaciones personales.
- Evento `join_chat` para mensajes en tiempo real en salas de chat.

## Licencia

MIT

---

**¿Preguntas o sugerencias?**  
Abre un issue en el repositorio o contactame.
