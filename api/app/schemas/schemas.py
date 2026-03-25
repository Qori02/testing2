from pydantic import BaseModel, ConfigDict
from typing import Any, Optional
from datetime import datetime
from decimal import Decimal
from app.models.models import MissionStatus, SensorTypeEnum, EquipmentType, EquipmentStatus, LogLevel


# ── Missions ────────────────────────────────────────────────────────────────

class MissionCreate(BaseModel):
    mission_name:        str
    mission_description: Optional[str] = None
    drone_type:          Optional[str] = None
    location:            Optional[str] = None
    start_time:          Optional[datetime] = None
    end_time:            Optional[datetime] = None
    status:              Optional[MissionStatus] = MissionStatus.PLANNED


class MissionStatusUpdate(BaseModel):
    status: MissionStatus


class MissionOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    mission_id:          int
    mission_name:        str
    mission_description: Optional[str]
    drone_type:          Optional[str]
    location:            Optional[str]
    start_time:          Optional[datetime]
    end_time:            Optional[datetime]
    status:              MissionStatus
    created_at:          Optional[datetime]
    updated_at:          Optional[datetime]


# ── Sensor Data ─────────────────────────────────────────────────────────────

class SensorDataCreate(BaseModel):
    sensor_type: SensorTypeEnum
    value:       str
    unit:        Optional[str] = None


class SensorDataOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    sensor_id:   int
    mission_id:  int
    sensor_type: SensorTypeEnum
    value:       str
    unit:        Optional[str]
    timestamp:   Optional[datetime]


# ── Detections ───────────────────────────────────────────────────────────────

class DetectionCreate(BaseModel):
    object_class: str
    confidence:   float
    bounding_box: Optional[dict[str, Any]] = None
    image_path:   Optional[str] = None


class DetectionOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    detection_id: int
    mission_id:   int
    object_class: str
    confidence:   Decimal
    bounding_box: Optional[dict[str, Any]]
    image_path:   Optional[str]
    timestamp:    Optional[datetime]


# ── Equipment ────────────────────────────────────────────────────────────────

class EquipmentOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    equipment_id:        int
    equipment_name:      str
    type:                Optional[EquipmentType]
    status:              Optional[EquipmentStatus]
    drone_compatibility: Optional[str]
    created_at:          Optional[datetime]


# ── System Logs ──────────────────────────────────────────────────────────────

class SystemLogCreate(BaseModel):
    level:   LogLevel
    message: str


class SystemLogOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    log_id:    int
    level:     LogLevel
    message:   str
    timestamp: Optional[datetime]