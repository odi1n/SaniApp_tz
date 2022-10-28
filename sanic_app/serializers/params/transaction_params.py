from pydantic import BaseModel, PositiveInt, Field


class TransactionParams(BaseModel):
    bill_id: PositiveInt = Field(description="Bill id")
    product_id: PositiveInt = Field(description="Product id")

    class Config:
        orm_mode = True
