from dataclasses import dataclass


@dataclass
class ResponseController:
    sucess: bool
    message: str