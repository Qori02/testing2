import enum
from sqlalchemy import Column, BigInteger, String, Text, Enum, TIMESTAMP, DECIMAL, ForeignKey, Index
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.db.base import Base


class MissionStatus(str, enum.Enum):
    PLANNED = "PLANNED"
    ACTIVE = "ACTIVE"
    COMPLETED = "COMPLETED"
    FAILED = "FAILED"


class SensorTypeEnum(str, enum.Enum):
    TEMPERATURE = "TEMPERATURE"
    HUMIDITY = "HUMIDITY"
    GPS = "GPS"
    LIDAR = "LIDAR"
    CAMERA = "CAMERA"
    PROXIMITY = "PROXIMITY"


class EquipmentType(str, enum.Enum):
    GRIPPER = "GRIPPER"
    CAMERA = "CAMERA"
    SENSOR = "SENSOR"
    SAMPLER = "SAMPLER"


class EquipmentStatus(str, enum.Enum):
    AVAILABLE = "AVAILABLE"
    IN_USE = "IN_USE"
    MAINTENANCE = "MAINTENANCE"


class LogLevel(str, enum.Enum):
    INFO = "INFO"
    WARNING = "WARNING"
    ERROR = "ERROR"


class Mission(Base):
    __tablename__ = "missions"

    mission_id          = Column(BigInteger, primary_key=True, autoincrement=True)
    mission_name        = Column(String(100), nullable=False)
    mission_description = Column(Text)
    drone_type          = Column(String(50))
    location            = Column(String(100))
    start_time          = Column(TIMESTAMP)
    end_time            = Column(TIMESTAMP)
    status              = Column(Enum(MissionStatus, name="mission_status"), default=MissionStatus.PLANNED)
    created_at          = Column(TIMESTAMP, server_default=func.now())
    updated_at          = Column(TIMESTAMP, server_default=func.now(), onupdate=func.now())

    sensor_data = relationship("SensorData", back_populates="mission", cascade="all, delete")
    detections  = relationship("Detection",  back_populates="mission", cascade="all, delete")


class SensorData(Base):
    __tablename__ = "sensor_data"

    sensor_id   = Column(BigInteger, primary_key=True, autoincrement=True)
    mission_id  = Column(BigInteger, ForeignKey("missions.mission_id", ondelete="CASCADE"))
    sensor_type = Column(Enum(SensorTypeEnum, name="sensor_type_enum"))
    value       = Column(String(255))
    unit        = Column(String(20))
    timestamp   = Column(TIMESTAMP, server_default=func.now())

    mission = relationship("Mission", back_populates="sensor_data")

    __table_args__ = (
        Index("idx_mission_time", "mission_id", "timestamp"),
    )


class Detection(Base):
    __tablename__ = "detections"

    detection_id = Column(BigInteger, primary_key=True, autoincrement=True)
    mission_id   = Column(BigInteger, ForeignKey("missions.mission_id", ondelete="CASCADE"))
    object_class = Column(String(50))
    confidence   = Column(DECIMAL(5, 4))
    bounding_box = Column(JSONB)
    image_path   = Column(String(500))
    timestamp    = Column(TIMESTAMP, server_default=func.now())

    mission = relationship("Mission", back_populates="detections")


class Equipment(Base):
    __tablename__ = "equipment"

    equipment_id        = Column(BigInteger, primary_key=True, autoincrement=True)
    equipment_name      = Column(String(100), nullable=False)
    type                = Column(Enum(EquipmentType,   name="equipment_type"))
    status              = Column(Enum(EquipmentStatus, name="equipment_status"))
    drone_compatibility = Column(String(100))
    created_at          = Column(TIMESTAMP, server_default=func.now())


class SystemLog(Base):
    __tablename__ = "system_logs"

    log_id    = Column(BigInteger, primary_key=True, autoincrement=True)
    level     = Column(Enum(LogLevel, name="log_level"))
    message   = Column(Text)
    timestamp = Column(TIMESTAMP, server_default=func.now())