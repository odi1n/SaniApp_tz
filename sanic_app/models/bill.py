from tortoise import Model, fields



class Bill(Model):
    uid = fields.IntField(pk=True)
    balance = fields.DecimalField(max_digits=10, decimal_places=2, default=0)
    user = fields.ForeignKeyField("models.User", related_name="score_user")

    class Meta:
        table: str = "bill"
