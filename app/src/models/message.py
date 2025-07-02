from datetime import datetime
from bson import ObjectId

class Message: 
    def __init__(self, _id: ObjectId = None, chat_id: ObjectId = None, type : str = "", content: str = "", timestamp: datetime = None, remitente_id: ObjectId = None):
        self.id = _id if _id else ObjectId()
        self.chat_id = chat_id
        self.type = type
        self.content = content
        self.timestamp = timestamp if timestamp else datetime.now()
        self.remitente_id = remitente_id

    def to_dict(self):
        # Para API: serializable
        return {
            "_id": str(self.id) if self.id else None,
            "chat_id": str(self.chat_id) if self.chat_id else None,
            "type": self.type,
            "content": self.content,
            "timestamp": self.timestamp if self.timestamp else None,
            "remitente_id": str(self.remitente_id) if self.remitente_id else None
        }

    def to_mongo_dict(self):
        # Para guardar en MongoDB: ObjectId
        return {
            "_id": self.id,
            "chat_id": self.chat_id,
            "type": self.type,
            "content": self.content,
            "timestamp": self.timestamp if self.timestamp else None,
            "remitente_id": self.remitente_id if self.remitente_id else None
        }

    @classmethod
    def from_dict(cls, data):
        timestamp = data.get("timestamp")
        if isinstance(timestamp, str):
            timestamp = datetime.fromisoformat(timestamp)
        # Si ya es datetime o None, lo deja igual

        return cls(
            _id=ObjectId(data["_id"]) if "_id" in data and ObjectId.is_valid(str(data["_id"])) else None,
            chat_id=ObjectId(data["chat_id"]) if "chat_id" in data and ObjectId.is_valid(str(data["chat_id"])) else None,
            type=data.get("type", ""),
            content=data.get("content", ""),
            timestamp=timestamp,
            remitente_id=ObjectId(data["remitente_id"]) if "remitente_id" in data and ObjectId.is_valid(str(data["remitente_id"])) else None
        )