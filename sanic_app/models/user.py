from uuid import uuid4

from tortoise import Model, fields


class User(Model):
    id = fields.IntField(pk=True)
    username = fields.CharField(max_length=50, unique=True)
    hashed_password = fields.CharField(max_length=255)
    is_active = fields.BooleanField(default=False)
    confirmation = fields.UUIDField(default=uuid4)

    class Meta:
        table: str = "user"

    def __str__(self):
        return f"User {self.id}: {self.username}"

    def to_dict(self):
        return {"user_id": self.id, "username": self.username}