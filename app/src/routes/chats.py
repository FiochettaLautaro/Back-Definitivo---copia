from datetime import datetime
from flask import Blueprint, request, jsonify
from bson.objectid import ObjectId
from src.models.chat import Chat
from src.db.connect import get_db_connection
from src.models.message import Message  
import boto3 # lib para subir archivos a S3
from bson.errors import InvalidId  # para manejar errores de ID inválidos

chats_bp = Blueprint('chats', __name__, url_prefix='/api/chats')
@chats_bp.route('/<uid>', methods=['GET']) # Obtener todos los chats de un usuario para la pantalla de chats
def get_chats(uid):
    try:
        db = get_db_connection()
        chats = db.chats.find({"participants": ObjectId(uid)})
        return jsonify([Chat.from_dict(chat).to_dict() for chat in chats]), 200
    except InvalidId:
        return jsonify({"error": "Invalid user ID"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
@chats_bp.route('/<chat_id>/<uid>', methods=['GET'])  # Obtener un chat específico
def get_chat(chat_id, uid):
    try:
        db = get_db_connection()
        chat = db.chats.find_one({"_id": ObjectId(chat_id), "participants": ObjectId(uid)})
        if chat:
            # Esto ejecuta tu from_dict y verás los prints
            chat_obj = Chat.from_dict(chat)
            messages = db.messages.find({"chat_id": ObjectId(chat_id)})

            db.messages.update_many({"remitente_id": ObjectId(uid), "chat_id": ObjectId(chat_id), "read": False}, {"$set": {"read": True}})
            return jsonify({
                "chat": chat_obj.to_dict(),
                "messages": [Message.from_dict(msg).to_dict() for msg in messages]
            }), 200
        return jsonify({"error": "Chat not found"}), 404
    except InvalidId:
        return jsonify({"error": "Invalid chat ID or user ID"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
@chats_bp.route('/<chat_id>/messages', methods=['POST'])  # Enviar un mensaje en un chat
def send_message(chat_id):
    try:
        db = get_db_connection()
        # Usar form-data para archivos y campos de texto
        remitente_id = request.form.get("remitente_id")
        type_ = request.form.get("type")
        content = request.form.get("content")
        file = request.files.get("file")

        if type_ not in ["text", "image", "video", "audio", "location", "file"]:
            return jsonify({"error": "Invalid message type"}), 400

        if not remitente_id:
            return jsonify({"error": "remitente_id is required"}), 400

        validarChat = db.chats.find_one({"_id": ObjectId(chat_id), "participants": ObjectId(remitente_id)})
        if validarChat is None:
            return jsonify({"error": "Chat not found or user not part of the chat"}), 404

        now = datetime.utcnow()
        if type_ in ["image", "video", "audio", "file"]:
            if not file:
                return jsonify({"error": "No se recibió archivo"}), 400
            url = upload_file(type_, chat_id)
            message = Message(
                chat_id=ObjectId(chat_id),
                remitente_id=ObjectId(remitente_id),
                content=url,
                type=type_,
                timestamp=now
            )
            db.messages.insert_one(message.to_mongo_dict())
            actualizar_chat = {
                "last_message": type_,
                "last_updated": now
            }
        else:
            if not content:
                return jsonify({"error": "content is required"}), 400
            message = Message(
                chat_id=ObjectId(chat_id),
                remitente_id=ObjectId(remitente_id),
                content=content,
                type=type_,
                timestamp=now
            )
            db.messages.insert_one(message.to_mongo_dict())
            actualizar_chat = {
                "last_message": content,
                "last_updated": now
            }
        db.chats.update_one({"_id": ObjectId(chat_id)}, {"$set": actualizar_chat})
        return jsonify({"message": "Message sent successfully"}), 201
    except InvalidId:
        return jsonify({"error": "Invalid chat ID or user ID"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
    
@chats_bp.route('/<uid1>/<uid2>', methods=['POST'])  # Crear un nuevo chat
def create_chat(uid1, uid2):
    try:
        db = get_db_connection()
        now = datetime.utcnow()
        chat = Chat(participants=[ObjectId(uid1), ObjectId(uid2)], created_at=now, last_message="-", last_updated=now)
        db.chats.insert_one(chat.to_dict())
        return jsonify({"message": "Chat created successfully", "chat_id": str(chat.id)}), 201
    except InvalidId:
        return jsonify({"error": "Invalid user ID"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    


def upload_file(file_type, chat_id): # Funcion para subir archivos a S3
    
    file = request.files.get('file')
    if not file:
        return jsonify({"error": "No se recibió archivo"}), 500

    if file_type not in ["image", "video", "audio", "file"]:
        return jsonify({"error": "Tipo de archivo no válido"}), 400
    
    # Subir a S3 (ejemplo)
    s3 = boto3.client('s3')
    bucket = 'superfix20'
    carpeta = f"Recursos Chats/{chat_id}/{file_type}"
    nombre_archivo = f"{carpeta}/{file.filename}"

    s3.upload_fileobj(file, bucket, nombre_archivo)

    url = f"https://{bucket}.s3.amazonaws.com/{nombre_archivo}"
    return url