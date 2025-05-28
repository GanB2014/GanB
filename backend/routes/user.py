from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from database import get_db
from models import User, Post, Comment
from routes.auth import get_current_user, UserInfo, create_access_token
from pydantic import BaseModel

router = APIRouter(
    prefix="/user",
    tags=["user"]
)

# 닉네임 변경용 스키마
class NicknameUpdate(BaseModel):
    nickname: str

#  닉네임 변경
@router.patch("/nickname")
def update_nickname(
    data: NicknameUpdate,
    db: Session = Depends(get_db),
    current_user: UserInfo = Depends(get_current_user)
):
    user = db.query(User).filter(User.id == current_user.id).first()
    if not user:
        raise HTTPException(status_code=404, detail="사용자를 찾을 수 없습니다.")
    
    user.nickname = data.nickname
    db.commit()
    db.refresh(user)

    #  닉네임 반영된 새 토큰 발급
    new_token = create_access_token({
        "sub": user.user_id,
        "nickname": user.nickname,
        "id": user.id,
        "is_admin": user.is_admin
    })

    return {
        "message": "닉네임이 변경되었습니다.",
        "nickname": user.nickname,
        "access_token": new_token
    }

#  내가 쓴 글 목록 조회
@router.get("/my-posts")
def get_my_posts(
    page: int = Query(1, ge=1),
    page_size: int = Query(8, ge=1),
    db: Session = Depends(get_db),
    current_user: UserInfo = Depends(get_current_user),
):
    query = db.query(Post).filter(Post.user_id == current_user.user_id)
    total = query.count()
    posts = query.order_by(Post.created_at.desc()).offset((page - 1) * page_size).limit(page_size).all()

    result = [
        {
            "id": post.id,
            "title": post.title,
            "created_at": post.created_at
        } for post in posts
    ]

    return {
        "posts": result,
        "total": total,
        "total_pages": (total + page_size - 1) // page_size,
        "current_page": page
    }

#  내가 쓴 댓글 목록 조회
@router.get("/my-comments")
def get_my_comments(
    page: int = Query(1, ge=1),
    page_size: int = Query(8, ge=1),
    db: Session = Depends(get_db),
    current_user: UserInfo = Depends(get_current_user),
):
    query = db.query(Comment).filter(Comment.user_id == current_user.id)
    total = query.count()
    comments = query.order_by(Comment.created_at.desc()).offset((page - 1) * page_size).limit(page_size).all()

    result = [
        {
            "id": comment.id,
            "content": comment.content,
            "created_at": comment.created_at
        } for comment in comments
    ]

    return {
        "comments": result,
        "total": total,
        "total_pages": (total + page_size - 1) // page_size,
        "current_page": page
    }
