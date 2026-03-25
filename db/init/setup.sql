
-- Enums
CREATE TYPE mission_status AS ENUM ('PLANNED', 'ACTIVE', 'COMPLETED', 'FAILED');
CREATE TYPE sensor_type_enum AS ENUM ('TEMPERATURE', 'HUMIDITY', 'GPS', 'LIDAR', 'CAMERA', 'PROXIMITY');
CREATE TYPE equipment_type AS ENUM ('GRIPPER', 'CAMERA', 'SENSOR', 'SAMPLER');
CREATE TYPE equipment_status AS ENUM ('AVAILABLE', 'IN_USE', 'MAINTENANCE');
CREATE TYPE log_level AS ENUM ('INFO', 'WARNING', 'ERROR');

-- Tables
CREATE TABLE missions (
    mission_id      BIGSERIAL PRIMARY KEY,
    mission_name    VARCHAR(100) NOT NULL,
    mission_description TEXT,
    drone_type      VARCHAR(50),
    location        VARCHAR(100),
    start_time      TIMESTAMP,
    end_time        TIMESTAMP,
    status          mission_status DEFAULT 'PLANNED',
    created_at      TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at      TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE sensor_data (
    sensor_id       BIGSERIAL PRIMARY KEY,
    mission_id      BIGINT REFERENCES missions(mission_id) ON DELETE CASCADE,
    sensor_type     sensor_type_enum,
    value           VARCHAR(255),
    unit            VARCHAR(20),
    timestamp       TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_mission_time ON sensor_data (mission_id, timestamp);

CREATE TABLE detections (
    detection_id    BIGSERIAL PRIMARY KEY,
    mission_id      BIGINT REFERENCES missions(mission_id) ON DELETE CASCADE,
    object_class    VARCHAR(50),
    confidence      DECIMAL(5,4),
    bounding_box    JSONB,
    image_path      VARCHAR(500),
    timestamp       TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE equipment (
    equipment_id        BIGSERIAL PRIMARY KEY,
    equipment_name      VARCHAR(100) NOT NULL,
    type                equipment_type,
    status              equipment_status,
    drone_compatibility VARCHAR(100),
    created_at          TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE system_logs (
    log_id      BIGSERIAL PRIMARY KEY,
    level       log_level,
    message     TEXT,
    timestamp   TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Sample data
INSERT INTO missions (mission_name, mission_description, status, drone_type, location) VALUES
('Bygningsinspeksjon A',  'Inspeksjon av tak og fasade',          'COMPLETED', 'DJI Mavic 3',         'Oslo sentrum'),
('Prøveinnsamling B',     'Biologisk prøveinnsamling i skog',     'ACTIVE',    'Custom Hexacopter',   'Nordmarka'),
('Kartlegging C',         '3D-kartlegging av konstruksjon',       'PLANNED',   'DJI Phantom',         'Fornebu'),
('Overvåking D',          'Overvåking av byggeplass',             'FAILED',    'Parrot Anafi',        'Bærum sentrum'),
('Miljøundersøkelse E',   'Luftkvalitetsmåling i urbane områder', 'COMPLETED', 'DJI Mavic Air 2',     'Grünerløkka, Oslo'),
('Redningsoperasjon F',   'Søk og redning i fjellterreng',        'ACTIVE',    'Custom Octocopter',   'Jotunheimen nasjonalpark');

INSERT INTO sensor_data (mission_id, sensor_type, value, unit) VALUES
(1, 'CAMERA',      'Image_001.jpg',        'N/A'),
(1, 'LIDAR',       '1500',                 'meters'),
(2, 'TEMPERATURE', '22.5',                 'Celsius'),
(2, 'HUMIDITY',    '60',                   'Percent'),
(3, 'GPS',         '59.911491, 10.757933', 'Coordinates'),
(4, 'PROXIMITY',   '5',                    'meters'),
(5, 'TEMPERATURE', '18.3',                 'Celsius'),
(6, 'CAMERA',      'Image_002.jpg',        'N/A');

INSERT INTO detections (mission_id, object_class, confidence, bounding_box) VALUES
(1, 'Person',   0.9876, '{"x": 100, "y": 150, "width": 50,  "height": 100}'),
(2, 'Vehicle',  0.8765, '{"x": 200, "y": 250, "width": 80,  "height": 60}'),
(3, 'Building', 0.7654, '{"x": 300, "y": 350, "width": 120, "height": 200}'),
(4, 'Animal',   0.6543, '{"x": 400, "y": 450, "width": 40,  "height": 80}'),
(5, 'Tree',     0.5432, '{"x": 500, "y": 550, "width": 60,  "height": 150}'),
(6, 'Person',   0.4321, '{"x": 600, "y": 650, "width": 50,  "height": 100}');

INSERT INTO equipment (equipment_id, equipment_name, type, status, drone_compatibility) VALUES
(1, 'High-Res Camera',        'CAMERA',  'IN_USE',     'DJI Mavic 3, DJI Phantom'),
(2, 'Thermal Sensor',         'SENSOR',  'AVAILABLE',  'Custom Hexacopter, Custom Octocopter'),
(3, 'Gripper Arm',            'GRIPPER', 'MAINTENANCE','Custom Hexacopter'),
(4, 'LIDAR Scanner',          'SENSOR',  'IN_USE',     'DJI Mavic Air 2, DJI Phantom'),
(5, 'Environmental Sampler',  'SAMPLER', 'AVAILABLE',  'Custom Octocopter');

