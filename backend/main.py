from fastapi import FastAPI
from routes import posts, upload, comments, auth, admin, notifications, user
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware


# 🔧 DB 테이블 자동 생성
from database import engine
from models import Base

# DB 테이블을 자동으로 생성
Base.metadata.create_all(bind=engine)

app = FastAPI()

# ✅ CORS 설정: 특정 도메인에서의 접근을 허용
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # React 클라이언트가 http://localhost:3000에서 동작한다고 가정
    allow_credentials=True,
    allow_methods=["*"],  # 모든 HTTP 메서드 허용
    allow_headers=["*"],  # 모든 HTTP 헤더 허용
)

# ✅ 라우터 등록: 게시글, 댓글, 파일 업로드 라우터를 앱에 포함
app.include_router(posts.router, tags=["posts"])
app.include_router(upload.router, tags=["uploads"])
app.include_router(comments.router, tags=["comments"])
app.include_router(auth.router, tags=["auth"])
app.include_router(admin.router) # 관리자 전용 라우터
app.include_router(notifications.router, tags=["notifications"])

# ✅ 업로드된 이미지 접근 가능하게 설정
# `/uploads` 경로로 업로드된 파일에 접근할 수 있도록 StaticFiles 설정
app.mount("/uploads", StaticFiles(directory="uploads"), name="uploads")

app.include_router(user.router, tags=["user"])
