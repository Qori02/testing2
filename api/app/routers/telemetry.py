from datetime import datetime, timezone
from typing import Optional
from fastapi import APIRouter, Depends, HTTPException, Query
from pydantic import BaseModel
from influxdb_client import Point
from app.db.influx import get_write_api, get_query_api
from app.core.config import INFLUX_BUCKET, INFLUX_ORG
from app.models.models import SensorTypeEnum

router = APIRouter(prefix="/missions/{mission_id}/telemetry", tags=["Telemetry (InfluxDB)"])


class TelemetryIn(BaseModel):
    sensor_type: SensorTypeEnum
    value:       float
    unit:        Optional[str] = None


class TelemetryOut(BaseModel):
    mission_id:  int
    sensor_type: str
    value:       float
    unit:        Optional[str]
    timestamp:   datetime



@router.post("", status_code=201)
def post_telemetry(mission_id: int, body: TelemetryIn):
    """Dronen sender en maling. Lagres i InfluxDB."""
    point = (
        Point("sensor_data")
        .tag("mission_id", str(mission_id))
        .tag("sensor_type", body.sensor_type.value)
        .tag("unit", body.unit or "")
        .field("value", body.value)
        .time(datetime.now(timezone.utc))
    )
    get_write_api().write(bucket=INFLUX_BUCKET, org=INFLUX_ORG, record=point)
    return {"status": "ok", "mission_id": mission_id, "sensor_type": body.sensor_type}


@router.get("", response_model=list[TelemetryOut])
def get_telemetry(
    mission_id: int,
    range_minutes: int = Query(default=60, description="Hent data fra de siste X minuttene"),
):
    """Henter telemetridata for et oppdrag fra InfluxDB."""
    query = f"""
        from(bucket: "drone_telemetry")
          |> range(start: -{range_minutes}m)
          |> filter(fn: (r) => r._measurement == "sensor_data")
          |> filter(fn: (r) => r.mission_id == "{mission_id}")
    """
    tables = get_query_api().query(query=query, org=INFLUX_ORG)

    results = []
    for table in tables:
        for record in table.records:
            results.append(TelemetryOut(
                mission_id=mission_id,
                sensor_type=record.values.get("sensor_type", ""),
                value=record.get_value(),
                unit=record.values.get("unit") or None,
                timestamp=record.get_time(),
            ))
    return results


@router.get("/latest", response_model=TelemetryOut)
def get_latest_telemetry(mission_id: int):
    """Henter den nyeste malingen for et oppdrag."""
    query = f"""
        from(bucket: "drone_telemetry")
          |> range(start: -24h)
          |> filter(fn: (r) => r._measurement == "sensor_data")
          |> filter(fn: (r) => r.mission_id == "{mission_id}")
          |> last()
    """
    tables = get_query_api().query(query=query, org=INFLUX_ORG)

    for table in tables:
        for record in table.records:
            return TelemetryOut(
                mission_id=mission_id,
                sensor_type=record.values.get("sensor_type", ""),
                value=record.get_value(),
                unit=record.values.get("unit") or None,
                timestamp=record.get_time(),
            )

    raise HTTPException(status_code=404, detail="Ingen telemetridata funnet for dette oppdraget")