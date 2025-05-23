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

### 백엔드 실행

```bash
cd backend
python -m venv venv
venv\Scripts\activate          # 윈도우 기준
pip install -r requirements.txt
uvicorn main:app --reload
```

### 프론트엔드 실행
```bash
cd frontend
npm install
npm start
```

### 📝 기타 사항
- MySQL 테이블 생성은 Alembic 또는 직접 models.py 기준으로 실행
- is_deleted가 True인 유저는 삭제된 유저로 간주하며 게시글/댓글에서 '탈퇴한 사용자'로 표시됨


- .env 파일에는 아래와 같은 정보가 들어가야 합니다:
```bash
- SECRET_KEY=your_secret
- ALGORITHM=HS256
- MYSQL_HOST=localhost
- MYSQL_PORT=3306
- MYSQL_USER=root
- MYSQL_PASSWORD=your_password
- MYSQL_DATABASE=gproject_db
```
