from tortoise import Model, fields
from tortoise.contrib.pydantic import pydantic_model_creator, pydantic_queryset_creator


class Product(Model):
    id = fields.IntField(pk=True)
    title = fields.CharField(max_length=150)
    description = fields.TextField()
    price: int = fields.DecimalField(max_digits=10, decimal_places=2, default=0)

    class Meta:
        table: str = "product"

    def __str__(self):
        return f"Product - {self.title}"


ProductModelCreate = pydantic_model_creator(Product, name="ProductModelCreate")
ProductPydanticOut = pydantic_queryset_creator(Product, name="ProductPydanticOut")
ProductPydanticIn = pydantic_model_creator(Product, name="ProductPydanticIn", exclude_readonly=True)
