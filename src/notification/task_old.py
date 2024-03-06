from tasks import app
from notification.entitys import ListContacts
from notification.controller import ChromeDriverController, WhatsappNotification
import time

contacts = ListContacts()

@app.task
def task_notification(number: str, message: str):
    driver = ChromeDriverController(False, True)
    wpp = WhatsappNotification(driver, contacts)
    wpp.send_message_new_contact(number, message)
    time.sleep(5)
    driver.driver.quit()

@app.task
def task_notification_group(message: str):
    driver = ChromeDriverController(False, True)
    wpp = WhatsappNotification(driver, contacts)
    contact = contacts.get_contact('default')
    wpp.send_message(contact, message)
    time.sleep(5)
    driver.driver.quit()
