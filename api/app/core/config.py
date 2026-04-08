import os

DATABASE_URL = os.getenv("DATABASE_URL", "")
if not DATABASE_URL:
    raise RuntimeError("DATABASE_URL environment variable is not set")

STORAGE_DIR = os.getenv("STORAGE_DIR", "/data")

INFLUX_URL    = os.getenv("INFLUX_URL", "")
INFLUX_TOKEN  = os.getenv("INFLUX_TOKEN", "")
INFLUX_ORG    = os.getenv("INFLUX_ORG", "")
INFLUX_BUCKET = os.getenv("INFLUX_BUCKET", "")

if not all([INFLUX_URL, INFLUX_TOKEN, INFLUX_ORG, INFLUX_BUCKET]):
    raise RuntimeError("En eller flere InfluxDB miljøvariabler mangler")
