from fastapi import APIRouter, UploadFile, Form
from glpi.controller import Archive, DatasRegister
from tasks import task_glpi_create

router = APIRouter()

@router.post("/glpi")
async def glpi_create(
    unity: str = Form(...),
    reason: str = Form(...),
    desc: str = Form(...),
    contact: str = Form(...),
    files: list[UploadFile] = None
):
    datas = DatasRegister(unity=unity, reason=reason, desc=desc, contact=contact)
    datas_dict = datas.model_dump()
    archives = [{"filename": file.filename, "content": await file.read()} for file in files] if files else []
    task_glpi_create.delay(datas_dict, archives)