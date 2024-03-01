import requests


def send_wpp_notification_grupo(message: str) -> bool:
  
    url = 'http://localhost:8001/send'
    data = {
        "number": "default",
        "message": message
    }
    response = requests.post(url, json=data)
    if response.status_code == 200:
        return True
    else:
        return False
    
def send_wpp_notification_number(number: str, message:str) -> bool:
    url = 'http://localhost:8001/sendNew'
    data = {
        "number": number,
        "message": message
    }
    response = requests.post(url, json=data)
    if response.status_code == 200:
        return True
    else:
        return False