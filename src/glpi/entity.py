from dataclasses import dataclass
from pydantic import BaseModel

@dataclass
class Archive:
    name: str
    bts: bytes


class DatasRegister(BaseModel):
    unity: str
    reason: str
    desc: str
    contact: str