from fastapi import APIRouter
from notification.entity import NotifyWpp
from notification.task import task_notification_wpp

router = APIRouter()

@router.post("/notification/wpp")
def notification_wpp(notify: NotifyWpp):
    task_notification_wpp.delay(notify.number, notify.message)