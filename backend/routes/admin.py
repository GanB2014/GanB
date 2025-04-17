from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from routes.auth import get_current_user, UserInfo
from models import User, Post, Comment, Notification
import os

router = APIRouter(
    prefix="/admin",
    tags=["admin"]
)

# ✅ 관리자 권한 확인 함수
def verify_admin(current_user: UserInfo):
    if not getattr(current_user, "is_admin", False):
        raise HTTPException(status_code=403, detail="관리자 권한이 필요합니다.")

# ✅ 관리자 대시보드 (간단한 접근 확인용)
@router.get("/dashboard")
def admin_dashboard(current_user: UserInfo = Depends(get_current_user)):
    verify_admin(current_user)
    return {"message": "관리자 대시보드 접근 성공", "nickname": current_user.nickname}

# ✅ 전체 사용자 조회 (삭제되지 않은 사용자만)
@router.get("/users")
def list_users(db: Session = Depends(get_db), current_user: UserInfo = Depends(get_current_user)):
    verify_admin(current_user)
    users = db.query(User).filter(User.is_deleted == False).all()
    return [
        {
            "id": u.id,
            "user_id": u.user_id,
            "nickname": u.nickname,
            "is_admin": u.is_admin,
            "is_active": u.is_active,
            "is_banned": u.is_banned
        }
        for u in users
    ]

# ✅ 회원 정지
@router.patch("/ban-user/{user_id}")
def ban_user(user_id: str, db: Session = Depends(get_db), current_user: UserInfo = Depends(get_current_user)):
    verify_admin(current_user)
    user = db.query(User).filter(User.user_id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="해당 사용자를 찾을 수 없습니다.")
    if user.is_admin:
        raise HTTPException(status_code=400, detail="관리자는 정지할 수 없습니다.")
    user.is_banned = 1
    db.commit()
    return {"message": f"{user.nickname} 계정을 정지시켰습니다."}

# ✅ 회원 정지 해제
@router.patch("/unban-user/{user_id}")
def unban_user(
    user_id: str,
    db: Session = Depends(get_db),
    current_user: UserInfo = Depends(get_current_user)
):
    verify_admin(current_user)
    user = db.query(User).filter(User.user_id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="해당 사용자를 찾을 수 없습니다.")
    if user.is_admin:
        raise HTTPException(status_code=400, detail="관리자는 정지 해제 대상이 아닙니다.")
    user.is_banned = 0
    db.commit()
    return {"message": f"{user.nickname} 계정의 정지를 해제했습니다."}

# ✅ 회원 삭제 (논리 삭제 방식)
@router.delete("/users/{user_id}")
def delete_user(user_id: str, db: Session = Depends(get_db), current_user: UserInfo = Depends(get_current_user)):
    verify_admin(current_user)
    user = db.query(User).filter(User.user_id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="해당 유저를 찾을 수 없습니다.")
    user.is_deleted = True
    db.commit()
    return {"message": f"{user_id} 계정이 삭제(표시)되었습니다."}

# ✅ 게시글 강제 삭제
@router.delete("/force-delete-post/{post_id}")
def force_delete_post(post_id: int, db: Session = Depends(get_db), current_user: UserInfo = Depends(get_current_user)):
    verify_admin(current_user)
    post = db.query(Post).filter(Post.id == post_id).first()
    if not post:
        raise HTTPException(status_code=404, detail="게시글을 찾을 수 없습니다.")
    if post.image_url:
        image_path = os.path.join("uploads", os.path.basename(post.image_url))
        if os.path.exists(image_path):
            os.remove(image_path)
    db.delete(post)
    db.commit()
    return {"message": f"게시글 {post_id}가 삭제되었습니다."}

# ✅ 댓글 강제 삭제 (알림 포함)
@router.delete("/force-delete-comment/{comment_id}")
def force_delete_comment(comment_id: int, db: Session = Depends(get_db), current_user: UserInfo = Depends(get_current_user)):
    verify_admin(current_user)
    comment = db.query(Comment).filter(Comment.id == comment_id).first()
    if not comment:
        raise HTTPException(status_code=404, detail="댓글을 찾을 수 없습니다.")

    # 🔁 관련 알림 먼저 삭제
    db.query(Notification).filter(Notification.comment_id == comment.id).delete()

    if comment.image_url:
        image_path = os.path.join("uploads", os.path.basename(comment.image_url))
        if os.path.exists(image_path):
            os.remove(image_path)
    db.delete(comment)
    db.commit()
    return {"message": f"댓글 {comment_id}가 삭제되었습니다."}

# ✅ 대댓글 강제 삭제 (알림 포함)
@router.delete("/force-delete-reply/{comment_id}")
def force_delete_reply(comment_id: int, db: Session = Depends(get_db), current_user: UserInfo = Depends(get_current_user)):
    verify_admin(current_user)
    reply = db.query(Comment).filter(Comment.id == comment_id, Comment.parent_id != None).first()
    if not reply:
        raise HTTPException(status_code=404, detail="대댓글을 찾을 수 없습니다.")

    # 🔁 관련 알림 먼저 삭제
    db.query(Notification).filter(Notification.comment_id == reply.id).delete()

    if reply.image_url:
        image_path = os.path.join("uploads", os.path.basename(reply.image_url))
        if os.path.exists(image_path):
            os.remove(image_path)
    db.delete(reply)
    db.commit()
    return {"message": f"대댓글 {comment_id}가 삭제되었습니다."}
