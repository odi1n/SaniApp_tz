from pydantic import BaseModel, Field


class Status(BaseModel):
    status: bool = Field(description="Status info", default=True)


class StatusLink(Status):
    link: str
