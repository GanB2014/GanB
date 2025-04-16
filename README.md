# 📌 커뮤니티 기반 SNS 웹사이트

## 📖 프로젝트 개요

로그인 기반의 게시판 커뮤니티 웹 애플리케이션입니다.  
회원은 글과 댓글을 작성하고, 관리자 계정은 사용자 관리, 게시글 및 댓글 강제 삭제 기능을 수행할 수 있습니다.  
사용자 간의 상호작용을 돕기 위해 알림 기능을 제공하며, 사용자 프로필에서는 작성한 글/댓글을 확인하고 닉네임을 변경할 수 있습니다.

---


## 📁 폴더 구조

```
📁 gproject/
├── 📁 backend/
│   ├── 📜 .env                        # 환경 변수 설정
│   ├── 📜 alembic.ini                 # Alembic 설정 파일
│   ├── 📜 requirements.txt            # Python 의존성
│   ├── 📜 database.py                 # DB 세션 및 연결
│   ├── 📜 main.py                     # FastAPI 진입점
│   ├── 📜 models.py                   # SQLAlchemy 모델
│   ├── 📜 schemas.py                  # Pydantic 스키마
│   ├── 📁 alembic/                    # 마이그레이션 폴더
│   ├── 📁 uploads/                    # 업로드된 이미지 저장
│   ├── 📁 venv/                       # 가상환경
│   └── 📁 routes/
│       ├── 📜 admin.py                # 관리자 기능
│       ├── 📜 auth.py                 # 로그인/회원가입
│       ├── 📜 comments.py             # 댓글/대댓글 기능
│       ├── 📜 notifications.py        # 알림 기능
│       ├── 📜 posts.py                # 게시글 CRUD
│       ├── 📜 upload.py               # 이미지 업로드
│       └── 📜 user.py                 # 프로필, 내 글/댓글

├── 📁 frontend/
│   ├── 📜 package.json                # npm 의존성 목록
│   ├── 📜 package-lock.json           # npm 버전 고정
│   ├── 📜 .gitignore                  # Git 무시 설정
│   ├── 📜 README.md                   # 프론트엔드 README
│   ├── 📁 public/                     # 정적 파일 (index.html 등)
│   ├── 📁 node_modules/               # 의존성 모듈
│   └── 📁 src/
│       ├── 📜 index.js                # 앱 진입점
│       ├── 📜 index.css               # 전체 스타일
│       ├── 📜 App.js                  # 라우팅 및 전체 구조
│       ├── 📁 api/                    # API 호출 모듈
│       ├── 📁 context/
│       │   └── 📜 AuthContext.js      # 로그인 상태 전역 관리
│       ├── 📁 components/
│       │   ├── 📜 NotificationDropdown.js  # 알림 드롭다운
│       │   ├── 📜 PostDetail.js       # 게시글 상세 (컴포넌트)
│       │   └── 📜 PostItem.js         # 게시글 목록 항목
│       └── 📁 pages/
│           ├── 📜 PostList.js         # 게시글 목록
│           ├── 📜 PostDetail.js       # 게시글 + 댓글 보기
│           ├── 📜 CreatePost.js       # 글 작성
│           ├── 📜 EditPost.js         # 글 수정
│           ├── 📜 MyProfile.js        # 내 글/댓글/닉네임 변경
│           ├── 📜 Register.js         # 회원가입
│           ├── 📜 Notifications.js    # 전체 알림 보기
│           ├── 📜 AdminUserPage.js    # 관리자 - 사용자 관리
│           └── 📜 AdminPostPage.js    # 관리자 - 게시글/댓글 관리

```


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
