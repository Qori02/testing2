Første bruk:
docker compose up -d --build

deretter 
docker compose ps

hvis ikke alle containere blir laget så kjør
docker compose up

for å avslutte så skriv
docker compose down

bare skriv
docker compose down -v
hvis du ønsker å fjerne all lagret data i databasen

For å ta i bruk API-en
http://localhost:8000/docs
Her kan du legge til eller fjerne data

Nyttige endepunkter
http://localhost:8000/health
http://localhost:8000/missions
http://localhost:8000/missions/1/telemetry
http://localhost:8000/missions/1/detections

For å kjøre testskriptet testdata.py kjør
python3 testdata.py 1 & python3 testdata.py 2 & 
Dette gjør det mulig å simulere testdata i både mission 1 og mission 2 samtidig