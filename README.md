# 📌 커뮤니티 기반 SNS 웹사이트

## 📖 프로젝트 개요

로그인 기반의 게시판 커뮤니티 웹 애플리케이션입니다.  
회원은 글과 댓글을 작성하고, 관리자 계정은 사용자 관리, 게시글 및 댓글 강제 삭제 기능을 수행할 수 있습니다.  
사용자 간의 상호작용을 돕기 위해 알림 기능을 제공하며, 사용자 프로필에서는 작성한 글/댓글을 확인하고 닉네임을 변경할 수 있습니다.

---


---

## 📁 폴더 구조


## ✅ Backend (/backend)
📦backend
 ┣ 📜.env                      # 환경 변수 설정 파일
 ┣ 📜alembic.ini              # Alembic 설정 파일 (마이그레이션 도구 설정)
 ┣ 📜requirements.txt         # 백엔드 패키지 의존성 목록
 ┣ 📜database.py              # DB 연결 및 SQLAlchemy 설정
 ┣ 📜main.py                  # FastAPI 앱 실행 파일 (라우터 등록 포함)
 ┣ 📜models.py                # SQLAlchemy ORM 모델 정의 (User, Post, Comment 등)
 ┣ 📜schemas.py               # Pydantic 스키마 정의 (요청/응답 모델)
 ┣ 📂uploads/                 # 업로드 이미지 저장 폴더
 ┣ 📂venv/                    # 가상환경 (제출 제외)
 ┗ 📂routes/                  # FastAPI 라우터 모듈들
   ┣ 📜admin.py               # 관리자 기능 (회원 정지/삭제, 게시글/댓글 강제 삭제 등)
   ┣ 📜auth.py                # 회원가입, 로그인 및 JWT 인증 관련 기능
   ┣ 📜comments.py            # 댓글/대댓글 작성, 조회, 수정, 삭제 및 알림 기능
   ┣ 📜notifications.py       # 알림 목록 조회, 읽음 처리, 삭제 기능
   ┣ 📜posts.py               # 게시글 CRUD 및 목록 조회 (검색, 페이지네이션 포함)
   ┣ 📜upload.py              # 파일 업로드 테스트용 (사용 안함)
   ┗ 📜user.py                # 닉네임 변경, 내가 쓴 글/댓글 목록 조회 기능


## ✅ Frontend (/frontend)
   📦frontend
 ┣ 📜.gitignore               # Git에 포함되지 않을 파일/폴더 설정
 ┣ 📜README.md                # 프론트엔드 관련 설명 (선택사항)
 ┣ 📜package.json             # 프론트엔드 패키지 의존성 목록
 ┣ 📜package-lock.json        # 패키지 버전 잠금 파일
 ┣ 📂public/                  # HTML 템플릿 등 공개 정적 파일
 ┗ 📂src/
   ┣ 📜index.js               # React 진입점 (ReactDOM 렌더링)
   ┣ 📜index.css              # 전체 스타일 초기화 및 설정
   ┣ 📜App.js                 # 전체 라우팅 구성
   ┣ 📂api/                   # Axios API 모듈 관리 (현재 비어있을 수 있음)
   ┣ 📂context/
   ┃ ┗ 📜AuthContext.js       # 로그인 상태 및 토큰 저장을 위한 전역 컨텍스트
   ┣ 📂components/
   ┃ ┣ 📜NotificationDropdown.js # 헤더 우측 알림 드롭다운 UI
   ┃ ┣ 📜PostDetail.js            # (이전 버전) 게시글 상세 내용 컴포넌트
   ┃ ┗ 📜PostItem.js              # 게시글 목록에서 한 개 항목을 나타내는 컴포넌트
   ┗ 📂pages/
     ┣ 📜PostList.js           # 게시글 목록 조회 및 검색, 페이지네이션
     ┣ 📜PostDetail.js         # 게시글 상세 페이지 (댓글/대댓글 포함)
     ┣ 📜CreatePost.js         # 게시글 작성 폼
     ┣ 📜EditPost.js           # 게시글 수정 폼
     ┣ 📜MyProfile.js          # 내 프로필 (닉네임 변경, 내가 쓴 글/댓글)
     ┣ 📜Register.js           # 회원가입 화면
     ┣ 📜Notifications.js      # 전체 알림 목록 확인 화면
     ┣ 📜AdminUserPage.js      # 관리자용 유저 목록 관리 (정지/삭제)
     ┗ 📜AdminPostPage.js      # (옵션) 관리자용 게시글 관리 페이지


---

## ✅ 주요 기능

### 👤 사용자 기능

- 회원가입 / 로그인
- 닉네임 변경
- 내가 쓴 글 / 댓글 목록 보기
- JWT 토큰 인증
- 댓글 및 대댓글 작성, 이미지 업로드
- 알림 기능 (게시글에 댓글, 댓글에 대댓글)

### 📝 게시글 기능

- 게시글 목록 / 상세 / 작성 / 수정 / 삭제
- 이미지 첨부
- 검색 (제목, 내용)
- 페이지네이션 처리 (게시글 10개씩)

### 💬 댓글 기능

- 댓글 / 대댓글 작성
- 이미지 업로드 포함
- 수정 / 삭제
- 댓글 트리 구조

### 📢 알림 기능

- 내 글에 댓글이 달리면 알림
- 내 댓글에 대댓글이 달리면 알림
- 읽음 처리 / 전체 확인 / 삭제 기능 포함

### 🔐 관리자 기능

- 회원 목록 조회
- 회원 정지 / 해제 / 삭제 (논리 삭제)
- 게시글 강제 삭제
- 댓글 / 대댓글 강제 삭제
- "탈퇴한 사용자"로 표시 처리

---

## ⚙️ 기술 스택

### Backend
- FastAPI
- MySQL
- SQLAlchemy + MySQL Connector
- JWT 인증
- Uvicorn
- Pydantic

### Frontend
- React
- React Router
- Bootstrap 5
- Axios
- Context API (AuthContext)

---

## 📦 실행 방법

### 🔧 백엔드 실행

```bash
cd backend
python -m venv venv
venv\Scripts\activate          # 윈도우 기준
pip install -r requirements.txt
uvicorn main:app --reload

### 🌐 프론트엔드 실행
```bash
cd frontend
npm install
npm start

.env 파일에는 아래와 같은 정보가 들어가야 합니다:

SECRET_KEY=your_secret
ALGORITHM=HS256
MYSQL_HOST=localhost
MYSQL_PORT=3306
MYSQL_USER=root
MYSQL_PASSWORD=your_password
MYSQL_DATABASE=gproject_db

📝 기타 사항
MySQL 테이블 생성은 Alembic 또는 직접 models.py 기준으로 실행

is_deleted가 True인 유저는 삭제된 유저로 간주하며 게시글/댓글에서 '탈퇴한 사용자'로 표시됨
