from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from models import Notification
from routes.auth import get_current_user, UserInfo
from typing import List, Optional
from pydantic import BaseModel
from datetime import datetime

router = APIRouter(
    prefix="/notifications",
    tags=["notifications"]
)

#  알림 응답 모델
class NotificationResponse(BaseModel):
    id: int
    type: str
    message: str
    post_id: Optional[int] = None     #  이 두 줄 추가
    comment_id: Optional[int] = None  # 
    is_read: bool
    created_at: datetime

    class Config:
        from_attributes = True

#  내 알림 목록 조회
@router.get("/", response_model=List[NotificationResponse])
def get_my_notifications(
    db: Session = Depends(get_db),
    current_user: UserInfo = Depends(get_current_user)
):
    notifs = db.query(Notification).filter(Notification.user_id == current_user.id).order_by(Notification.created_at.desc()).all()
    return notifs

from fastapi import Path

#  알림 읽음 처리
@router.patch("/read/{notification_id}")
def mark_notification_as_read(
    notification_id: int = Path(..., description="읽음 처리할 알림의 ID"),
    db: Session = Depends(get_db),
    current_user: UserInfo = Depends(get_current_user)
):
    notification = db.query(Notification).filter(
        Notification.id == notification_id,
        Notification.user_id == current_user.id
    ).first()

    if not notification:
        raise HTTPException(status_code=404, detail="알림을 찾을 수 없습니다.")

    if notification.is_read:
        return {"message": "이미 읽은 알림입니다."}

    notification.is_read = True
    db.commit()
    return {"message": " 알림이 읽음 처리되었습니다."}

#  전체 알림 읽음 처리
@router.patch("/read-all")
def mark_all_notifications_as_read(
    db: Session = Depends(get_db),
    current_user: UserInfo = Depends(get_current_user)
):
    notifications = db.query(Notification).filter(
        Notification.user_id == current_user.id,
        Notification.is_read == False
    ).all()

    for notif in notifications:
        notif.is_read = True

    db.commit()
    return {
        "message": " 모든 알림이 읽음 처리되었습니다.",
        "updated": len(notifications)
    }

#  읽지 않은 알림 개수 조회
@router.get("/unread-count")
def get_unread_notification_count(
    db: Session = Depends(get_db),
    current_user: UserInfo = Depends(get_current_user)
):
    count = db.query(Notification).filter(
        Notification.user_id == current_user.id,
        Notification.is_read == False
    ).count()
    return {"unread_count": count}

#  전체 알림 삭제
@router.delete("/all")
def delete_all_notifications(
    db: Session = Depends(get_db),
    current_user: UserInfo = Depends(get_current_user)
):
    deleted_count = db.query(Notification).filter(
        Notification.user_id == current_user.id
    ).delete()

    db.commit()

    return {"message": f" 모든 알림이 삭제되었습니다. (총 {deleted_count}개)"}

#  개별 알림 삭제
@router.delete("/{notification_id}")
def delete_notification(
    notification_id: int,
    db: Session = Depends(get_db),
    current_user: UserInfo = Depends(get_current_user)
):
    notification = db.query(Notification).filter(
        Notification.id == notification_id,
        Notification.user_id == current_user.id
    ).first()

    if not notification:
        raise HTTPException(status_code=404, detail="알림을 찾을 수 없습니다.")

    db.delete(notification)
    db.commit()

    return {"message": " 알림이 삭제되었습니다."}





