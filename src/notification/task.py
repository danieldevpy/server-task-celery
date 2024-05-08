from tasks import app
import requests

@app.task(bind=True, max_retries=5, retry_delay=120)
def task_notification(self, number: str, message: str):
    url = 'http://192.168.1.232:8006/sendNew'
    data = {
        "number": number,
        "message": message
    }
    response = requests.post(url, json=data)
    response_message = response.json()['msg']
    if response.status_code == 200:
        return response_message
    else:
        raise Exception(response_message)

@app.task(bind=True, max_retries=5, retry_delay=120)
def task_notification_group(self, message: str):
    url = 'http://192.168.1.232:8006/send'
    data = {
        "number": "default",
        "message": message
    }
    response = requests.post(url, json=data)
    response_message = response.json()['msg']
    if response.status_code == 200:
        return response_message
    else:
        raise Exception(response_message)