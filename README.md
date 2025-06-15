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
│   ├── 📜 .env.example                # 환경 변수 샘플 파일 (버전 관리)
│   ├── 📜 alembic.ini                 # Alembic 설정 파일 (마이그레이션 도구)
│   ├── 📜 requirements.txt            # 백엔드 의존성 목록
│   ├── 📜 database.py                 # DB 연결 및 세션 관리
│   ├── 📜 main.py                     # FastAPI 앱 진입점
│   ├── 📜 models.py                   # SQLAlchemy 모델 정의
│   ├── 📜 schemas.py                  # Pydantic 스키마 정의
│   ├── 📁 alembic/                    # DB 마이그레이션 파일들
│   ├── 📁 uploads/                    # 업로드된 이미지 저장 디렉토리
│   └── 📁 routes/                     # API 라우터 모음
│       ├── 📜 admin.py                # 관리자 기능 API
│       ├── 📜 auth.py                 # 회원가입 및 로그인 API
│       ├── 📜 comments.py             # 댓글 및 대댓글 API
│       ├── 📜 notifications.py        # 알림 기능 API
│       ├── 📜 posts.py                # 게시글 CRUD API
│       ├── 📜 upload.py               # 이미지 업로드 API
│       └── 📜 user.py                 # 사용자 프로필 및 작성글/댓글 API

├── 📁 frontend/
│   ├── 📜 package.json                # 프론트엔드 의존성 정의
│   ├── 📜 package-lock.json           # 의존성 버전 고정
│   ├── 📜 .gitignore                  # Git에서 제외할 파일 설정
│   ├── 📜 README.md                   # 프론트엔드 설명 문서
│   ├── 📁 public/                     # 정적 리소스 (index.html 등)
│   ├── 📁 node_modules/               # 설치된 npm 패키지
│   └── 📁 src/
│       ├── 📜 index.js                # 앱 렌더링 진입점
│       ├── 📜 index.css               # 전역 CSS 스타일
│       ├── 📜 App.js                  # 전체 라우팅 및 레이아웃 구성
│       ├── 📁 api/                    # 백엔드 API 호출 함수 정의
│       ├── 📁 context/
│       │   └── 📜 AuthContext.js      # 로그인 상태 관리 컨텍스트
│       ├── 📁 components/
│       │   ├── 📜 NotificationDropdown.js  # 알림 드롭다운 UI
│       │   ├── 📜 PostDetail.js       # 게시글 + 댓글 컴포넌트
│       │   └── 📜 PostItem.js         # 게시글 리스트의 단일 항목
│       └── 📁 pages/
│           ├── 📜 PostList.js         # 게시글 목록 페이지
│           ├── 📜 PostDetail.js       # 게시글 상세 페이지 (댓글 포함)
│           ├── 📜 CreatePost.js       # 게시글 작성 페이지
│           ├── 📜 EditPost.js         # 게시글 수정 페이지
│           ├── 📜 MyProfile.js        # 내 글/댓글/닉네임 변경 페이지
│           ├── 📜 Register.js         # 회원가입 페이지
│           ├── 📜 Notifications.js    # 전체 알림 보기
│           ├── 📜 AdminUserPage.js    # 관리자 - 유저 관리 페이지
│           └── 📜 AdminPostPage.js    # 관리자 - 게시글 및 댓글 관리

```


---


### 구성
|게시글 목록 #1|회원가입 #2|로그인 #3|
|:---:|:---:|:---:|
|![1  게시글 목록2](https://github.com/user-attachments/assets/098a976b-ab3d-4357-84b7-c1d98094740a)|![2  회원가입](https://github.com/user-attachments/assets/ddaf51d0-025e-43fa-8f8d-b7180d8e2773)|![3  게시글 목록](https://github.com/user-attachments/assets/f16e27bb-bfd7-45d6-ab14-18cbe446e3a6)|


|글 작성 #4|게시글 내용 #5|알림 #6|전체알림 #7|
|:---:|:---:|:---:|:---:|
|![4  글 작성](https://github.com/user-attachments/assets/77922e9d-ab1f-49c6-bdd0-32ec0d94fc19)|![5  게시글 내용](https://github.com/user-attachments/assets/ebb27a21-c194-4c72-8b54-f9be7280056a)|![6  알림](https://github.com/user-attachments/assets/b455bc59-a65a-4771-8c68-a03b80f20e68)|![6 1 전체알림](https://github.com/user-attachments/assets/97f9528f-352c-4765-b23b-0f0f991b1677)|


|프로필 #8|관리자 #9|게시글 정렬 #10|게시글 정렬2 #11|
|:---:|:---:|:---:|:---:|
|![7  프로필](https://github.com/user-attachments/assets/ec0bdf25-2f53-4633-9247-8ef8c0d2ae9e)|![8  관리자](https://github.com/user-attachments/assets/a8f605e2-7826-412d-a39f-3d93192e04ae)|![9  최신순](https://github.com/user-attachments/assets/047effb4-4d18-4fff-8f9e-54dae214f0cf)|![10  오래된 순](https://github.com/user-attachments/assets/fe4496d9-a9a1-42ac-a492-dc6f18148e8a)|



---

## ✅ 주요 기능

### 👤 사용자 기능

- 회원가입 (아이디, 비밀번호, 닉네임)
- 로그인 (JWT 발급 및 전역 상태 저장)

### 🙋‍♂️ 마이페이지 기능

- 닉네임 변경
- 내가 쓴 게시글 목록 (페이지네이션: 8개씩)
- 내가 쓴 댓글 목록 (페이지네이션: 8개씩)

### 📝 게시글 기능

- 게시글 작성 (제목, 내용, 이미지 포함 가능)
- 게시글 수정 (텍스트/이미지 변경 가능)
- 게시글 삭제 (작성자 또는 관리자)
- 게시글 목록 조회
  - 검색 (제목 + 내용)
  - 정렬 (최신순, 오래된순, 제목순)
  - 페이지네이션
- 게시글 상세 보기

### 💬 댓글/대댓글 기능

- 댓글 작성 (이미지 첨부 가능)
- 댓글 수정/삭제 (작성자 또는 관리자)
- 대댓글 작성 (이미지 첨부 가능)
- 대댓글 수정/삭제 (작성자 또는 관리자)
- 트리 구조로 댓글 및 대댓글 표시

### 🖼️ 이미지 업로드

- 업로드된 이미지 /uploads/ 폴더에 저장
- 수정/삭제 시 기존 이미지 삭제 처리

### 🔔 알림 기능

- 게시글에 댓글이 달리면 글 작성자에게 알림 전송
- 댓글에 대댓글이 달리면 댓글 작성자에게 알림 전송
- 알림 목록 조회
- 알림 읽음 처리
- 알림 개수 카운트
- 알림 삭제

### 🛠 관리자 기능

- 관리자 계정만 접근 가능
- 사용자 목록 조회
- 사용자 정지 / 정지 해제
- 사용자 삭제 (논리 삭제: `is_deleted = True`)
- 게시글 강제 삭제 (작성자 관계 없이 삭제 가능)
- 댓글 강제 삭제 (작성자 관계 없이 삭제 가능)
- 대댓글 강제 삭제 (작성자 관계 없이 삭제 가능)

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
```

### 🌐 프론트엔드 실행
```bash
cd frontend
npm install
npm start
```

### 📝 기타 사항
- MySQL 테이블 생성은 Alembic 또는 직접 models.py 기준으로 실행
- is_deleted가 True인 유저는 삭제된 유저로 간주하며 게시글/댓글에서 '탈퇴한 사용자'로 표시됨

- 환경변수 설정은 `backend/.env.example` 파일을 참고하여 `.env` 파일을 생성하세요.
- `.env` 파일은 보안상 버전 관리에서 제외됩니다.
