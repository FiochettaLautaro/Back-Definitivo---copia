from datetime import datetime
from bson import ObjectId

class Chat:
    def __init__(self, _id: ObjectId = None, participants: list = None, created_at: datetime = None, last_message: str = None, last_updated: datetime = None):
        self.id = _id if _id else ObjectId()
        self.participants = participants if participants else []
        self.created_at = created_at if created_at else datetime.now()
        self.last_message = last_message
        self.last_updated = last_updated

    def to_dict(self):
        return {
            "_id": str(self.id) if self.id else None,
            "participants": [str(p) for p in self.participants],
            "created_at": self.created_at,
            "last_message": self.last_message,
            "last_updated": self.last_updated
        }

    @classmethod
    def from_dict(cls, data):
        created_at = data.get("created_at")
        if isinstance(created_at, str):
            created_at = datetime.fromisoformat(created_at)
        # Si ya es datetime o None, lo deja igual

        last_updated = data.get("last_updated")
        if isinstance(last_updated, str):
            last_updated = datetime.fromisoformat(last_updated)
        # Si ya es datetime o None, lo deja igual

        #print("created_at:", created_at, type(created_at))
        #print("last_updated:", last_updated, type(last_updated))

        return cls(
            _id=ObjectId(data["_id"]) if "_id" in data and ObjectId.is_valid(str(data["_id"])) else None,
            participants=data.get("participants", []),
            created_at=created_at,
            last_message=data.get("last_message", ""),
            last_updated=last_updated
        )