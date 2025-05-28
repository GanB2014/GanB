from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from passlib.context import CryptContext
from database import get_db
from pydantic import BaseModel
from models import User
from datetime import datetime, timedelta
from jose import jwt, JWTError
from fastapi.security import OAuth2PasswordBearer

#  비밀번호 암호화 설정
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

#  JWT 설정
SECRET_KEY = "your_secret_key"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 1440

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")

router = APIRouter(
    prefix="/auth",
    tags=["auth"]
)

#  Pydantic 모델 정의
class UserCreate(BaseModel):
    user_id: str
    password: str
    nickname: str

class UserLogin(BaseModel):
    user_id: str
    password: str

class UserInfo(BaseModel):
    id: int
    user_id: str
    nickname: str
    is_admin: bool
    is_banned: bool

#  비밀번호 처리
def hash_password(password: str) -> str:
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

#  JWT 토큰 생성
def create_access_token(data: dict, expires_delta: timedelta = None) -> str:
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=15))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

#  회원가입 API
@router.post("/register")
def signup(user: UserCreate, db: Session = Depends(get_db)):
    if len(user.user_id) > 16 or len(user.password) > 20 or len(user.nickname) > 16:
        raise HTTPException(status_code=400, detail="입력값 길이 제한 초과")

    if db.query(User).filter(User.user_id == user.user_id).first():
        raise HTTPException(status_code=400, detail="아이디가 이미 존재합니다.")
    if db.query(User).filter(User.nickname == user.nickname).first():
        raise HTTPException(status_code=400, detail="닉네임이 이미 존재합니다.")

    hashed_pw = hash_password(user.password)
    new_user = User(user_id=user.user_id, hashed_password=hashed_pw, nickname=user.nickname)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return {"message": "회원가입 성공"}

#  로그인 API
@router.post("/login")
def login(user: UserLogin, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(
        User.user_id == user.user_id,
        User.is_deleted == False  #  탈퇴하지 않은 사용자만 로그인 가능
    ).first()

    if not db_user or not verify_password(user.password, db_user.hashed_password):
        raise HTTPException(status_code=400, detail="아이디 또는 비밀번호 오류")

    if db_user.is_active == 0:
        raise HTTPException(status_code=403, detail="비활성화된 계정입니다.")
    if db_user.is_banned == 1:
        raise HTTPException(status_code=403, detail="정지된 계정입니다.")

    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={
            "id": db_user.id,
            "sub": db_user.user_id,
            "nickname": db_user.nickname,
            "is_admin": db_user.is_admin,
            "is_banned": db_user.is_banned
        },
        expires_delta=access_token_expires
    )

    return {
        "access_token": access_token,
        "token_type": "bearer",
        "nickname": db_user.nickname,
        "is_admin": db_user.is_admin
    }

#  현재 사용자 정보 가져오기 (의존성)
def get_current_user(db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)) -> UserInfo:
    credentials_exception = HTTPException(
        status_code=401,
        detail="사용자 인증에 실패했습니다.",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id = payload.get("sub")
        user_pk = payload.get("id")
        nickname = payload.get("nickname")
        is_admin = payload.get("is_admin", False)
        is_banned = payload.get("is_banned", False)

        if user_id is None or user_pk is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception

    user = db.query(User).filter(
        User.id == user_pk,
        User.user_id == user_id,
        User.is_deleted == False  #  탈퇴한 유저는 인증 실패 처리
    ).first()

    if user is None:
        raise credentials_exception

    if user.is_banned:
        raise HTTPException(status_code=403, detail="정지된 계정은 접근할 수 없습니다.")

    return UserInfo(
        id=user.id,
        user_id=user.user_id,
        nickname=user.nickname,
        is_admin=user.is_admin,
        is_banned=user.is_banned
    )

#  닉네임 변경 API
@router.put("/change-nickname")
def change_nickname(new_nickname: str, db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=401,
        detail="사용자 인증에 실패했습니다.",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id = payload.get("sub")
        user_pk = payload.get("id")
    except JWTError:
        raise credentials_exception

    user = db.query(User).filter(User.id == user_pk, User.user_id == user_id).first()
    if user is None:
        raise credentials_exception

    user.nickname = new_nickname
    db.commit()
    db.refresh(user)

    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={
            "id": user.id,
            "sub": user.user_id,
            "nickname": user.nickname,
            "is_admin": user.is_admin,
            "is_banned": user.is_banned
        },
        expires_delta=access_token_expires
    )

    return {
        "access_token": access_token,
        "token_type": "bearer",
        "nickname": user.nickname
    }
