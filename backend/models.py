from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Text, Boolean
from sqlalchemy import func
from sqlalchemy.orm import relationship, DeclarativeBase
from datetime import datetime
from database import engine


class Root(DeclarativeBase):
    pass


# 📌 User 모델 (사용자)
class User(Root):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(String(16), unique=True, nullable=False)
    hashed_password = Column(String(128), nullable=False)
    nickname = Column(String(16), unique=True, nullable=False)
    is_admin = Column(Integer, default=0)
    is_active = Column(Integer, default=1)  # ✅ 정지 여부 추가
    is_banned = Column(Integer, default=0)  # 0: 정상, 1: 정지
    is_deleted = Column(Boolean, default=False)


    posts = relationship("Post", back_populates="owner")
    comments = relationship("Comment", back_populates="owner")


# 📌 Post 모델 (게시글)
class Post(Root):
    __tablename__ = "posts"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), nullable=False)  # 제목
    content = Column(Text, nullable=False)  # 내용
    image_url = Column(String(255), nullable=True)  # 이미지 URL
    created_at = Column(DateTime, default=datetime.utcnow)  # 작성 시간
    user_id = Column(String(16), ForeignKey("users.user_id"), nullable=False)  # user_id로 수정

    owner = relationship("User", back_populates="posts")
    comments = relationship("Comment", back_populates="post", cascade="all, delete")


# 📌 Comment 모델 (댓글)
class Comment(Root):
    __tablename__ = "comments"

    id = Column(Integer, primary_key=True, index=True)
    post_id = Column(Integer, ForeignKey("posts.id"))
    content = Column(Text, nullable=False)  # 댓글 내용
    image_url = Column(String(255), nullable=True)  # 댓글 이미지 URL
    parent_id = Column(Integer, ForeignKey("comments.id"), nullable=True)  # 부모 댓글 ID (대댓글)
    created_at = Column(DateTime, default=datetime.utcnow)  # 댓글 작성 시간
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    nickname = Column(String(16), nullable=False)  # 문자열 컬럼으로 닉네임 저장

    post = relationship("Post", back_populates="comments")
    parent = relationship("Comment", remote_side=[id], backref="replies")
    owner = relationship("User", back_populates="comments")

# 📌 Notification 모델 (알림)
class Notification(Root):
    __tablename__ = "notifications"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)  # 알림을 받을 사용자
    type = Column(String(50))  # 예: "comment_on_post", "reply_on_comment"
    message = Column(String(255))
    post_id = Column(Integer, ForeignKey("posts.id"), nullable=True)
    comment_id = Column(Integer, ForeignKey("comments.id"), nullable=True)
    is_read = Column(Integer, default=0)  # 0: 안읽음, 1: 읽음
    created_at = Column(DateTime, default=datetime.utcnow)

    user = relationship("User", backref="notifications")

def create_all_database():
    print("Load auto generation schema...")
    print(Root.metadata.tables.keys())
    Root.metadata.create_all(bind=engine)