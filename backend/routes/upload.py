from fastapi import APIRouter, File, UploadFile, HTTPException
import shutil
import os
from uuid import uuid4

router = APIRouter()

#  이미지 저장 경로
UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

#  이미지 업로드 API
@router.post("/upload/")
async def upload_image(file: UploadFile = File(...)):
    try:
        #  파일 확장자 확인
        ext = file.filename.split(".")[-1]
        if ext.lower() not in ["jpg", "jpeg", "png", "gif"]:
            raise HTTPException(status_code=400, detail=" 지원하지 않는 이미지 형식입니다.")

        #  파일 저장 (랜덤 파일명 사용)
        filename = f"{uuid4().hex}.{ext}"
        file_path = os.path.join(UPLOAD_DIR, filename)
        
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        #  업로드된 이미지 URL 반환
        return {"image_url": f"http://127.0.0.1:8001/uploads/{filename}"}
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f" 이미지 업로드 실패: {str(e)}")
