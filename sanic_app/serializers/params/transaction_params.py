from pydantic import BaseModel, PositiveInt, Field


class TransactionParams(BaseModel):
    score_id: PositiveInt = Field(description="Score id")
    product_id: PositiveInt = Field(description="Product id")
    amount: PositiveInt = Field(description="Amount")

    class Config:
        orm_mode = True