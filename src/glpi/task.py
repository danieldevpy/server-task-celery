from typing import List
from tasks import app
from controller.driver import ChromeDriverController
from glpi.controller import GLPIFunctions, DatasRegister, Archive
from notification.task import task_notification_group
from controller.bckp import BackupErros

@app.task(bind=True, max_retries=3)
def task_glpi_create(self, datas: dict, files: List[dict]=None):
    retries = self.request.retries
    new_datas = DatasRegister(**datas)
    driver = ChromeDriverController(hadless=True, cache=False)
    glpi = GLPIFunctions(driver)
    glpi.login()

    if retries:
        if retries == 0:
            archives = [Archive(file["filename"], file["content"]) for file in files] if files else []
            response = glpi.open_request(new_datas, archives)
        else:
            response = glpi.open_request(new_datas)

    else:
        archives = [Archive(file["filename"], file["content"]) for file in files] if files else []
        response = glpi.open_request(new_datas, archives)

    if response.sucess:
        task_notification_group.delay(response.message)
        return "Chamado aberto com sucesso"
    else:
        task_notification_group.delay("Algum erro ao abrir o chamado no glpi, confira nas tasks do flower")
        raise Exception(response.message)
    

