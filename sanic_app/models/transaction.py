from tortoise import Model, fields
from tortoise.contrib.pydantic import pydantic_model_creator, pydantic_queryset_creator


class Transaction(Model):
    bill = fields.ForeignKeyField("models.Bill", related_name="transaction_score")
    product = fields.ForeignKeyField("models.Product", related_name="transaction_product")

    class Meta:
        table: str = "transaction"


TransactionPydanticOut = pydantic_model_creator(Transaction, name="TransactionPydanticOut")
TransactionQueryCreate = pydantic_queryset_creator(Transaction, name="TransactionQueryCreate")
