from fastapi import APIRouter, HTTPException, Form, File, UploadFile, Query, Depends
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import datetime
import os
import uuid

from database import get_db
from models import Comment, Post, Notification, User
from schemas import CommentResponse
from routes.auth import get_current_user, UserInfo

router = APIRouter(
    prefix="/comments",
    tags=["comments"]
)

UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

# ✅ 댓글 작성
@router.post("/", response_model=CommentResponse)
async def create_comment(
    content: str = Form(...),
    post_id: int = Form(...),
    parent_id: Optional[int] = Form(None),
    file: Optional[UploadFile] = File(None),
    db: Session = Depends(get_db),
    current_user: UserInfo = Depends(get_current_user)
):
    post = db.query(Post).filter(Post.id == post_id).first()
    if not post:
        raise HTTPException(status_code=404, detail="게시글을 찾을 수 없습니다.")

    if parent_id:
        parent_comment = db.query(Comment).filter(Comment.id == parent_id).first()
        if not parent_comment:
            raise HTTPException(status_code=404, detail="부모 댓글을 찾을 수 없습니다.")

    image_url = None
    if file:
        ext = file.filename.split(".")[-1]
        filename = f"{uuid.uuid4().hex}.{ext}"
        filepath = os.path.join(UPLOAD_DIR, filename)
        with open(filepath, "wb") as buffer:
            buffer.write(await file.read())
        image_url = f"/uploads/{filename}"

    new_comment = Comment(
        content=content,
        post_id=post_id,
        parent_id=parent_id,
        image_url=image_url,
        created_at=datetime.utcnow(),
        user_id=current_user.id,
        nickname=current_user.nickname
    )

    db.add(new_comment)
    db.flush()

    # 🔔 알림 생성
    if parent_id:
        parent_comment = db.query(Comment).filter(Comment.id == parent_id).first()
        if parent_comment and parent_comment.user_id != current_user.id:
            db.add(Notification(
                user_id=parent_comment.user_id,
                type="reply_on_comment",
                message=f"{current_user.nickname}님이 대댓글을 남겼습니다.",
                post_id=post.id,
                comment_id=new_comment.id,
                is_read=False,
                created_at=datetime.utcnow()
            ))
    else:
        post_owner = db.query(User).filter(User.user_id == post.user_id).first()
        if post_owner and post_owner.id != current_user.id:
            db.add(Notification(
                user_id=post_owner.id,
                type="comment_on_post",
                message=f"{current_user.nickname}님이 게시글에 댓글을 남겼습니다.",
                post_id=post.id,
                comment_id=new_comment.id,
                is_read=False,
                created_at=datetime.utcnow()
            ))

    db.commit()
    db.refresh(new_comment)
    return new_comment

# ✅ 댓글 트리 조회
@router.get("/{post_id}", response_model=List[CommentResponse])
def get_comments(post_id: int, db: Session = Depends(get_db)):
    all_comments = db.query(Comment).filter(Comment.post_id == post_id).all()

    for comment in all_comments:
        if not comment.nickname:
            comment.nickname = "탈퇴한 사용자"

    comment_dict = {comment.id: comment for comment in all_comments}
    root_comments = []

    for comment in all_comments:
        comment.replies = []

    for comment in all_comments:
        if comment.parent_id:
            parent = comment_dict.get(comment.parent_id)
            if parent:
                parent.replies.append(comment)
        else:
            root_comments.append(comment)

    return root_comments

# ✅ 댓글 삭제
@router.delete("/{comment_id}")
def delete_comment(
    comment_id: int,
    db: Session = Depends(get_db),
    current_user: UserInfo = Depends(get_current_user)
):
    comment = db.query(Comment).filter(Comment.id == comment_id).first()
    if not comment:
        raise HTTPException(status_code=404, detail="댓글을 찾을 수 없습니다.")
    if comment.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="댓글 삭제 권한이 없습니다.")

    # 🔁 관련 알림 먼저 삭제
    db.query(Notification).filter(Notification.comment_id == comment.id).delete()

    if comment.image_url:
        image_path = os.path.join(UPLOAD_DIR, os.path.basename(comment.image_url))
        if os.path.exists(image_path):
            os.remove(image_path)

    db.delete(comment)
    db.commit()
    return {"message": "✅ 댓글이 삭제되었습니다."}

# ✅ 대댓글 삭제
@router.delete("/reply/{comment_id}")
def delete_reply(
    comment_id: int,
    db: Session = Depends(get_db),
    current_user: UserInfo = Depends(get_current_user)
):
    comment = db.query(Comment).filter(Comment.id == comment_id, Comment.parent_id != None).first()
    if not comment:
        raise HTTPException(status_code=404, detail="대댓글을 찾을 수 없습니다.")
    if comment.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="대댓글 삭제 권한이 없습니다.")

    # 🔁 관련 알림 먼저 삭제
    db.query(Notification).filter(Notification.comment_id == comment.id).delete()

    if comment.image_url:
        image_path = os.path.join(UPLOAD_DIR, os.path.basename(comment.image_url))
        if os.path.exists(image_path):
            os.remove(image_path)

    db.delete(comment)
    db.commit()
    return {"message": "✅ 대댓글이 삭제되었습니다."}

# ✅ 댓글 수정
@router.patch("/{comment_id}", response_model=CommentResponse)
async def update_comment(
    comment_id: int,
    content: Optional[str] = Form(None),
    file: Optional[UploadFile] = File(None),
    db: Session = Depends(get_db),
    current_user: UserInfo = Depends(get_current_user)
):
    comment = db.query(Comment).filter(Comment.id == comment_id).first()
    if not comment:
        raise HTTPException(status_code=404, detail="댓글을 찾을 수 없습니다.")
    if comment.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="댓글 수정 권한이 없습니다.")

    if content:
        comment.content = content

    if file:
        if comment.image_url:
            old_path = os.path.join(UPLOAD_DIR, os.path.basename(comment.image_url))
            if os.path.exists(old_path):
                os.remove(old_path)
        ext = file.filename.split(".")[-1]
        filename = f"{uuid.uuid4().hex}.{ext}"
        filepath = os.path.join(UPLOAD_DIR, filename)
        with open(filepath, "wb") as buffer:
            buffer.write(await file.read())
        comment.image_url = f"/uploads/{filename}"

    db.commit()
    db.refresh(comment)
    return comment

# ✅ 댓글 ID로 조회
@router.get("/comment/{comment_id}", response_model=CommentResponse)
def get_comment_by_id(comment_id: int, db: Session = Depends(get_db)):
    comment = db.query(Comment).filter(Comment.id == comment_id).first()
    if not comment:
        raise HTTPException(status_code=404, detail="댓글을 찾을 수 없습니다.")
    if not comment.nickname:
        comment.nickname = "탈퇴한 사용자"
    return comment

# ✅ 전체 댓글 목록 조회
@router.get("/", response_model=List[CommentResponse])
def get_all_comments(db: Session = Depends(get_db)):
    comments = db.query(Comment).all()
    for c in comments:
        if not c.nickname:
            c.nickname = "탈퇴한 사용자"
    return comments
