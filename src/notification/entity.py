from pydantic import BaseModel


class NotifyWpp(BaseModel):
    number: str
    message: str