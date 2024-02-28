from dataclasses import dataclass
from pydantic import BaseModel


class DadosAPI(BaseModel):
    name: str
    cpf: str
    cargo: str
    contact: str

@dataclass
class Error:
    e: bool
    msg: str = None


@dataclass
class DadosFormSSO:
    name: str
    cpf: str
    cargo: str

    def get_index(self) -> int:
        match self.cargo:
            case 'Medico':
                return 15
            case 'Enfermeiro':
                return 11