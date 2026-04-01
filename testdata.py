#test

import requests
import time
import random 
import sys
import math 

api_url ="http://localhost:8000"
mission_id = int(sys.argv[1]) if len(sys.argv) > 1 else int(input("Mission ID: "))

def send(sensor_type: str, value: float, unit: str):
    response=requests.post(
        f"{api_url}/missions/{mission_id}/telemetry",
        json={
            "sensor_type": sensor_type,
            "value": value,
            "unit": unit,
        }
    )
    if response.status_code == 201:
        print(f"  + {sensor_type:<12} {round(value, 2):>8} {unit}")
    else:
        print(f"  - {sensor_type} feilet: {response.status_code}")

temp = 18.0
total = 60
step = 0
interval =2

print(f"Sender {total} målinger til mission {mission_id}")
print(f"Intervall: {interval} sekund mellom hver\n")

for i in range(total):
    step +=1
    print(f"Måling {i+1}/{total}:")
    temp += random.uniform(-0.3, 0.5)
    temp = max(10.0, min(35.0, temp))
    send("TEMPERATURE", temp, "Celsius")

    if i < total -1:
        time.sleep(interval)