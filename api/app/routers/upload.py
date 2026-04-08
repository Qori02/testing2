from fastapi import APIRouter, UploadFile, File, Depends
from sqlalchemy.orm import Session
import os
import shutil
 
from app.db.deps import get_db
from app.models.models import Detection
 
router = APIRouter(prefix="/upload", tags=["Upload"])
 
IMAGE_DIR = "/data/images"
VIDEO_DIR = "/data/videos"
 
# sørg for at mapper finnes
os.makedirs(IMAGE_DIR, exist_ok=True)
os.makedirs(VIDEO_DIR, exist_ok=True)
 
 
@router.post("/image/{mission_id}")
def upload_image(mission_id: int, file: UploadFile = File(...), db: Session = Depends(get_db)):
    file_path = os.path.join(IMAGE_DIR, file.filename)
 
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
 
    detection = Detection(
        mission_id=mission_id,
        object_class="unknown",
        confidence=0.0,
        image_path=file.filename
    )
 
    db.add(detection)
    db.commit()
 
    return {"message": "Image uploaded", "filename": file.filename}
 
 
@router.post("/video/{mission_id}")
def upload_video(mission_id: int, file: UploadFile = File(...)):
    file_path = os.path.join(VIDEO_DIR, file.filename)
 
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
 
    return {"message": "Video uploaded", "filename": file.filename}
 
from fastapi.responses import FileResponse
 
@router.get("/image/{filename}")
def get_image(filename: str):
    return FileResponse(f"/data/images/{filename}")
 
@router.get("/video/{filename}")
def get_video(filename: str):
    return FileResponse(f"/data/videos/{filename}")