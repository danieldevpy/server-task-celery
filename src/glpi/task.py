from typing import List
from tasks import app, states
from controller.driver import ChromeDriverController
from glpi.controller import GLPIFunctions, DatasRegister, Archive
from notification.task import task_notification_group

@app.task
def task_glpi_create(datas: dict, files: List[dict]=None):
        new_datas = DatasRegister(**datas)
        archives = [Archive(file["filename"], file["content"]) for file in files] if files else []
        driver = ChromeDriverController(hadless=True, cache=False)
        glpi = GLPIFunctions(driver)
        glpi.login()
        response = glpi.open_request(new_datas, archives)
        if response.sucess:
            task_notification_group.delay(response.message)
            return "Chamado aberto com sucesso"
        else:
            task_notification_group.delay("Algum erro ao abrir o chamado no glpi, confira nas taks")
            raise Exception(response.message)