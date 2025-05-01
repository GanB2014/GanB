from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session, declarative_base
import os
from dotenv import load_dotenv
import mysql.connector

# .env 파일 로드
load_dotenv()

# 환경 변수에서 DB 설정 가져오기
# TODO: dotenv 대신 configparser 사용
DB_USER = os.getenv('DB_USER')
DB_PASSWORD = os.getenv('DB_PASSWORD')
DB_HOST = os.getenv('DB_HOST')
DB_PORT = os.getenv('DB_PORT')
DB_NAME = os.getenv('DB_NAME')

# SQLAlchemy용 DB URL
DB_URL = f"mysql+mysqlconnector://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

# SQLAlchemy 엔진 및 세션 설정
engine = create_engine(DB_URL, echo=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base 클래스 생성 (한 번만 정의)
Base = declarative_base()

# ✅ MySQL Connector 방식 (MySQL 직접 연결용)
def get_connection():
    """
    MySQL Connector를 사용하여 데이터베이스에 직접 연결
    """
    try:
        print(DB_URL)
        conn = mysql.connector.connect(
            user=DB_USER,
            password=DB_PASSWORD,
            host=DB_HOST,
            port=DB_PORT,
            database=DB_NAME
        )
        return conn
    except:
        pass

# ✅ SQLAlchemy 세션 의존성 함수 (SQLAlchemy 세션용)
def get_db():
    """
    SQLAlchemy 세션을 반환하는 의존성 함수
    """
    db: Session = SessionLocal()
    try:
        yield db
    finally:
        db.close()
