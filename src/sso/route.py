from fastapi import APIRouter
from fastapi.responses import JSONResponse
from task import task_sso_create
import json, base64
from sso.entity import DadosAPI
from controller.wpp import send_wpp_notification_grupo

router = APIRouter()


@router.post("/sso")
async def sso_create(datas: DadosAPI):
    objeto_json = {"name": datas.name, "cpf": datas.cpf, "cargo": datas.cargo, "contact": datas.contact}
    json_codificado = base64.b64encode(json.dumps(objeto_json).encode('utf-8')).decode('utf-8')
    send_wpp_notification_grupo(f"*Solicitação de criação de login no sistema SSO* Para criar automaticamente, acesse o link abaixo\nhttp://localhost:8000/sso/{json_codificado}")
    return JSONResponse(json_codificado)
    
@router.get("/sso/{hash}")
async def sso_create(hash: str):
    json_decodificado = json.loads(base64.b64decode(hash).decode('utf-8'))
    name = json_decodificado['name']
    cpf = json_decodificado['cpf']
    cargo = json_decodificado['cargo']
    contact = json_decodificado['contact']
    task_sso_create.delay(name, cpf, cargo, contact)
    return 'O login está sendo criado!'
    