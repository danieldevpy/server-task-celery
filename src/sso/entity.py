from dataclasses import dataclass

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
        print(self.cargo)
        match self.cargo:
            case 'Medico':
                return 15
            case 'Enfermeiro':
                return 11
            case _:
                raise Exception('Cargo não encontrado')