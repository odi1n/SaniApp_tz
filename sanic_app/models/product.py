from tortoise import Model, fields


class Product(Model):
    id = fields.IntField(pk=True)
    title = fields.CharField(max_length=150)
    description = fields.TextField()
    price = fields.DecimalField(max_digits=10, decimal_places=2, default=0)

    class Meta:
        table: str = "product"

    def __str__(self):
        return f"Product - {self.title}"
