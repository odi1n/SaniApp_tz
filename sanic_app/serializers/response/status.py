from pydantic import BaseModel


class Status(BaseModel):
    status: bool


class StatusLink(Status):
    link: str
