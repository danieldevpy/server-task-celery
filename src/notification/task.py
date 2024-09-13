from tasks import app
import requests

@app.task(bind=True, max_retries=50, retry_delay=30)
def task_notification_wpp(self, number: str, message: str):
    url = 'http://192.168.1.10:8006/notification/wpp'
    data = {
        "number": number,
        "message": message
    }
    try:
        response = requests.post(url, json=data)
        response_message = response.json()['msg']
        if response.status_code == 200:
            return response_message
        else:
            raise Exception(response_message)
    except Exception as exc:
        self.retry(exc=exc)