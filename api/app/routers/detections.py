from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Form
from sqlalchemy.orm import Session
from typing import Optional
from pathlib import Path
import uuid
import json
from app.db.deps import get_db
from app.models.models import Mission, Detection
from app.schemas.schemas import DetectionOut
from fastapi.responses import FileResponse
import shutil
from app.schemas.schemas import DetectionCreate, DetectionOut
import os

router = APIRouter(prefix="/missions/{mission_id}/detections", tags=["Detections"])

IMAGE_DIR = "/data/images"
VIDEO_DIR = "/data/videos"

os.makedirs(IMAGE_DIR, exist_ok=True)
os.makedirs(VIDEO_DIR, exist_ok=True)



def _get_mission_or_404(mission_id: int, db: Session) -> Mission:
    mission = db.get(Mission, mission_id)
    if not mission:
        raise HTTPException(status_code=404, detail="Mission not found")
    return mission


@router.post("", response_model=DetectionOut, status_code=201)
def add_detection(
    mission_id: int,
    object_class: str,
    confidence: float,
    bounding_box: Optional[str],
    file: Optional[UploadFile],
    db: Session = Depends (get_db),
):
    
    _get_mission_or_404(mission_id, db)
    saved_path = None
    if file is not None:
        file_path = os.path.join(IMAGE_DIR, file.filename)
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
        saved_path = file_path

    bbox = None
    if bounding_box:
        try:
            bbox = json.loads(bounding_box)
        except Exception:
            raise HTTPException(status_code=400, details="Test")
    
    detection = Detection(
        mission_id=mission_id,
        object_class=object_class,
        confidence=confidence,
        bounding_box=bbox,
        image_path=saved_path,
    )
    db.add(detection)
    db.commit()
    db.refresh(detection)
    return detection


@router.get("", response_model=list[DetectionOut])
def list_detections(mission_id: int, db: Session = Depends(get_db)):
    _get_mission_or_404(mission_id, db)
    return (
        db.query(Detection)
        .filter(Detection.mission_id == mission_id)
        .order_by(Detection.timestamp.desc())
        .all()
    )
