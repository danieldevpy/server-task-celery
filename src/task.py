from celery import Celery
from controller.driver import ChromeDriverController
from glpi.controller import GLPIFunctions, DatasRegister, Archive
from sso.controller import SSOFunctions, DadosFormSSO
from typing import List
from celery.backends.database import DatabaseBackend


app = Celery(
    'tasks',
    broker='pyamqp://guest@localhost//'
)
app.conf.update(
    result_backend='db+sqlite:///results.sqlite',
    result_serializer='json',
)

app.conf.database_engine_options = {'echo': True} 

@app.task
def task_glpi_create(datas: dict, files: List[dict]=None):
    new_datas = DatasRegister(**datas)
    archives = [Archive(file["filename"], file["content"]) for file in files] if files else []
    driver = ChromeDriverController(hadless=True, cache=False)
    glpi = GLPIFunctions(driver)
    glpi.login()
    glpi.open_request(new_datas, archives)
    return True

@app.task
def task_sso_create(name: str, cpf: str, cargo: str, contact: str):
    driver = ChromeDriverController(hadless=True, cache=False)
    sso = SSOFunctions(driver)
    sso.login()
    sso.create(DadosFormSSO(name=name, cpf=cpf, cargo=cargo), contact)