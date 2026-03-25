from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db.deps import get_db
from app.models.models import Mission
from app.schemas.schemas import MissionCreate, MissionOut, MissionStatusUpdate

router = APIRouter(prefix="/missions", tags=["Missions"])

@router.post("", response_model=MissionOut, status_code=201)
def create_mission(body: MissionCreate, db: Session = Depends(get_db)):
    mission = Mission(**body.model_dump())
    db.add(mission)
    db.commit()
    db.refresh(mission)
    return mission


@router.get("", response_model=list[MissionOut])
def list_missions(db: Session = Depends(get_db)):
    return db.query(Mission).order_by(Mission.created_at.desc()).all()


@router.get("/{mission_id}", response_model=MissionOut)
def get_mission(mission_id: int, db: Session = Depends(get_db)):
    mission = db.get(Mission, mission_id)
    if not mission:
        raise HTTPException(status_code=404, detail="Mission not found")
    return mission


@router.patch("/{mission_id}/status", response_model=MissionOut)
def update_status(mission_id: int, body: MissionStatusUpdate, db: Session = Depends(get_db)):
    mission = db.get(Mission, mission_id)
    if not mission:
        raise HTTPException(status_code=404, detail="Mission not found")
    mission.status = body.status
    db.commit()
    db.refresh(mission)
    return mission


@router.delete("/{mission_id}", status_code=204)
def delete_mission(mission_id: int, db: Session = Depends(get_db)):
    mission = db.get(Mission, mission_id)
    if not mission:
        raise HTTPException(status_code=404, detail="Mission not found")
    db.delete(mission)
    db.commit()