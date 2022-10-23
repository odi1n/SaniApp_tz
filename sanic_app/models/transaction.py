from tortoise import Model, fields

class Transaction(Model):
    score = fields.ForeignKeyField("models.Score", related_name="transaction_score")
    amount = fields.DecimalField(max_digits=10, decimal_places=2, default=0)

    class Meta:
        table: str = "transaction"
