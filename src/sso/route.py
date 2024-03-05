from fastapi import APIRouter
from fastapi.responses import JSONResponse
from task import task_sso_create
import json, base64

router = APIRouter()

@router.get("/sso/{hash}")
async def sso_create(hash: str):
    json_decodificado = json.loads(base64.b64decode(hash).decode('utf-8'))
    name = json_decodificado['name']
    cpf = json_decodificado['cpf']
    cargo = json_decodificado['cargo']
    contact = json_decodificado['contact']
    print(cargo)
    task_sso_create.delay(name, cpf, cargo, contact)
    return 'O login está sendo criado!'
    