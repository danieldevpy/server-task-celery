from celery.exceptions import Ignore
from tasks import app
from sso.controller import SSOFunctions, DadosFormSSO
from controller.driver import ChromeDriverController
from notification.task import task_notification, task_notification_group


@app.task
def task_sso_create(name: str, cpf: str, cargo: str, contact: str):
    driver = ChromeDriverController(hadless=True, cache=False)
    sso = SSOFunctions(driver)
    sso.login()
    datas = DadosFormSSO(name=name, cpf=cpf, cargo=cargo)
    response = sso.create(datas)
    if response.sucess:
        task_notification.delay(contact, response.message)
        return response.message
    else:
        task_notification_group.delay(response.message)
        raise Exception(response.message)