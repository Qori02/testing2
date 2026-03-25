from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db.deps import get_db
from app.models.models import Mission, Detection
from app.schemas.schemas import DetectionCreate, DetectionOut

router = APIRouter(prefix="/missions/{mission_id}/detections", tags=["Detections"])


def _get_mission_or_404(mission_id: int, db: Session) -> Mission:
    mission = db.get(Mission, mission_id)
    if not mission:
        raise HTTPException(status_code=404, detail="Mission not found")
    return mission


@router.post("", response_model=DetectionOut, status_code=201)
def add_detection(mission_id: int, body: DetectionCreate, db: Session = Depends(get_db)):
    _get_mission_or_404(mission_id, db)
    detection = Detection(mission_id=mission_id, **body.model_dump())
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