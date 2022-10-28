from pydantic import BaseModel, Field, PositiveInt


class WebhookParams(BaseModel):
    signature: str = Field(description="Signature line",
                           example="f4eae5b2881d8b6a1455f62502d08b2258d80084",
                           max_length=42, min_length=40)
    transaction_id: PositiveInt = Field(description="Transaction ID")
    user_id: PositiveInt = Field(description="User ID")
    bill_id: PositiveInt = Field(description="Bill ID")
    amount: PositiveInt = Field(description="Amount")
