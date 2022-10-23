from tortoise import Model, fields


class User(Model):
    id = fields.IntField(pk=True)
    login = fields.CharField(max_length=50, unique=True)
    hashed_password = fields.CharField(null=True, max_length=255)
    is_active = fields.BooleanField(null=False, default=False)
    confirmation = fields.UUIDField(null=True)

    class Meta:
        table: str = "user"

    def __str__(self):
        return f"User {self.id}: {self.login}"