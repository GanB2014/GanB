from fastapi import APIRouter, HTTPException, Form, File, UploadFile, Query, Depends
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import datetime
import os
import uuid
import math
from database import get_connection
from routes.auth import get_current_user, UserInfo
from pydantic import BaseModel

router = APIRouter()

UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

class PostBase(BaseModel):
    title: str
    content: str
    image_url: Optional[str] = None

# ✅ 게시글 작성
@router.post("/posts/")
async def create_post_with_image(
    title: str = Form(...),
    content: str = Form(...),
    file: UploadFile = File(None),
    current_user: UserInfo = Depends(get_current_user)
):
    conn = get_connection()
    if conn:
        cursor = conn.cursor(dictionary=True)
        image_url = None

        if file:
            ext = file.filename.split(".")[-1]
            filename = f"{uuid.uuid4().hex}.{ext}"
            filepath = os.path.join(UPLOAD_DIR, filename)
            with open(filepath, "wb") as buffer:
                buffer.write(await file.read())
            image_url = f"/uploads/{filename}"

        try:
            insert_query = "INSERT INTO posts (title, content, nickname, user_id, image_url) VALUES (%s, %s, %s, %s, %s)"
            cursor.execute(insert_query, (title, content, current_user.nickname, current_user.user_id, image_url))
            conn.commit()
            post_id = cursor.lastrowid
            cursor.execute("SELECT * FROM posts WHERE id = %s", (post_id,))
            return cursor.fetchone()
        except Exception as e:
            conn.rollback()
            raise HTTPException(status_code=500, detail=f"게시글 추가 실패: {str(e)}")
        finally:
            cursor.close()
            conn.close()
    raise HTTPException(status_code=500, detail="데이터베이스 연결 실패")

# ✅ 게시글 목록 조회
@router.get("/posts/")
def get_posts(
    page: int = Query(1, ge=1),
    page_size: int = Query(10, le=100),
    keyword: Optional[str] = Query(None),
    order: str = Query("newest", enum=["newest", "oldest", "title"])
):
    conn = get_connection()
    if conn:
        cursor = conn.cursor(dictionary=True)
        order_by = {
            "newest": "p.created_at DESC",
            "oldest": "p.created_at ASC",
            "title": "p.title ASC"
        }[order]
        offset = (page - 1) * page_size

        if keyword:
            query = f"""
                SELECT p.*, 
                    CASE WHEN u.is_deleted = 1 THEN '탈퇴한 사용자' ELSE u.nickname END AS nickname
                FROM posts p
                LEFT JOIN users u ON p.user_id = u.user_id
                WHERE p.title LIKE %s OR p.content LIKE %s
                ORDER BY {order_by}
                LIMIT %s OFFSET %s
            """
            cursor.execute(query, (f"%{keyword}%", f"%{keyword}%", page_size, offset))
        else:
            query = f"""
                SELECT p.*, 
                    CASE WHEN u.is_deleted = 1 THEN '탈퇴한 사용자' ELSE u.nickname END AS nickname
                FROM posts p
                LEFT JOIN users u ON p.user_id = u.user_id
                ORDER BY {order_by}
                LIMIT %s OFFSET %s
            """
            cursor.execute(query, (page_size, offset))
        posts = cursor.fetchall()

        if keyword:
            count_query = "SELECT COUNT(*) AS total FROM posts WHERE title LIKE %s OR content LIKE %s"
            cursor.execute(count_query, (f"%{keyword}%", f"%{keyword}%"))
        else:
            cursor.execute("SELECT COUNT(*) AS total FROM posts")
        total_count = cursor.fetchone()["total"]
        total_pages = math.ceil(total_count / page_size)

        cursor.close()
        conn.close()

        return {
            "posts": posts,
            "total_count": total_count,
            "total_pages": total_pages,
            "current_page": page,
            "page_size": page_size
        }

    raise HTTPException(status_code=500, detail="데이터베이스 연결 실패")

# ✅ 게시글 단일 조회
@router.get("/posts/{post_id}")
def get_post(post_id: int):
    conn = get_connection()
    if conn:
        cursor = conn.cursor(dictionary=True)
        query = """
            SELECT p.*, 
                CASE WHEN u.is_deleted = 1 THEN '탈퇴한 사용자' ELSE u.nickname END AS nickname
            FROM posts p
            LEFT JOIN users u ON p.user_id = u.user_id
            WHERE p.id = %s
        """
        cursor.execute(query, (post_id,))
        post = cursor.fetchone()
        cursor.close()
        conn.close()
        if post:
            return post
        raise HTTPException(status_code=404, detail="게시글을 찾을 수 없습니다.")
    raise HTTPException(status_code=500, detail="데이터베이스 연결 실패")

# ✅ 게시글 삭제
@router.delete("/posts/{post_id}")
def delete_post(post_id: int, current_user: UserInfo = Depends(get_current_user)):
    conn = get_connection()
    if conn:
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM posts WHERE id = %s", (post_id,))
        post = cursor.fetchone()
        if not post:
            cursor.close()
            conn.close()
            raise HTTPException(status_code=404, detail="게시글을 찾을 수 없습니다.")
        if post["user_id"] != current_user.user_id:
            cursor.close()
            conn.close()
            raise HTTPException(status_code=403, detail="게시글 삭제 권한이 없습니다.")
        if post["image_url"]:
            image_path = os.path.join(UPLOAD_DIR, os.path.basename(post["image_url"]))
            if os.path.exists(image_path):
                os.remove(image_path)
        try:
            cursor.execute("DELETE FROM posts WHERE id = %s", (post_id,))
            conn.commit()
            return {"message": "게시글이 삭제되었습니다!"}
        except Exception as e:
            conn.rollback()
            raise HTTPException(status_code=500, detail=f"게시글 삭제 실패: {str(e)}")
        finally:
            cursor.close()
            conn.close()
    raise HTTPException(status_code=500, detail="데이터베이스 연결 실패")

# ✅ 게시글 수정
@router.patch("/posts/{post_id}")
async def update_post(
    post_id: int,
    title: Optional[str] = Form(None),
    content: Optional[str] = Form(None),
    file: Optional[UploadFile] = File(None),
    current_user: UserInfo = Depends(get_current_user)
):
    conn = get_connection()
    if conn:
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM posts WHERE id = %s", (post_id,))
        existing_post = cursor.fetchone()
        if not existing_post:
            cursor.close()
            conn.close()
            raise HTTPException(status_code=404, detail="게시글을 찾을 수 없습니다.")
        if existing_post["user_id"] != current_user.user_id:
            cursor.close()
            conn.close()
            raise HTTPException(status_code=403, detail="게시글 수정 권한이 없습니다.")

        updated_title = title or existing_post["title"]
        updated_content = content or existing_post["content"]
        updated_image_url = existing_post["image_url"]

        if file:
            if updated_image_url:
                old_image_path = os.path.join(UPLOAD_DIR, os.path.basename(updated_image_url))
                if os.path.exists(old_image_path):
                    os.remove(old_image_path)
            ext = file.filename.split(".")[-1]
            filename = f"{uuid.uuid4().hex}.{ext}"
            filepath = os.path.join(UPLOAD_DIR, filename)
            with open(filepath, "wb") as buffer:
                buffer.write(await file.read())
            updated_image_url = f"/uploads/{filename}"

        cursor.execute(
            "UPDATE posts SET title = %s, content = %s, image_url = %s WHERE id = %s",
            (updated_title, updated_content, updated_image_url, post_id)
        )
        conn.commit()
        cursor.execute("SELECT * FROM posts WHERE id = %s", (post_id,))
        updated_post = cursor.fetchone()
        cursor.close()
        conn.close()
        return updated_post

    raise HTTPException(status_code=500, detail="데이터베이스 연결 실패")
