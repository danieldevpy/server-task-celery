from tasks import app
import requests

@app.task(bind=True)
def task_notification(self, number: str, message: str):
    url = 'http://localhost:8001/sendNew'
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

@app.task(bind=True)
def task_notification_group(self, message: str):
    url = 'http://localhost:8001/send'
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