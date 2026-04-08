-- Enums
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

CREATE TYPE mission_status AS ENUM ('PLANNED', 'ACTIVE', 'COMPLETED', 'FAILED');
CREATE TYPE equipment_type AS ENUM ('GRIPPER', 'CAMERA', 'SENSOR', 'SAMPLER');
CREATE TYPE equipment_status AS ENUM ('AVAILABLE', 'IN_USE', 'MAINTENANCE');
CREATE TYPE log_level AS ENUM ('INFO', 'WARNING', 'ERROR');

-- Tables
CREATE TABLE missions (
    mission_id          BIGSERIAL PRIMARY KEY,
    mission_name        VARCHAR(100) NOT NULL,
    mission_description TEXT,
    drone_type          VARCHAR(50),
    location            VARCHAR(100),
    start_time          TIMESTAMP,
    end_time            TIMESTAMP,
    status              mission_status DEFAULT 'PLANNED',
    created_at          TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at          TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

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

-- Genome experimental feature
CREATE TABLE genomic_samples (
    id          UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    mission_id  BIGINT REFERENCES missions(mission_id) ON DELETE CASCADE,
    sample_id   VARCHAR(100) UNIQUE NOT NULL,
    file_path   VARCHAR(500) NOT NULL,  -- sti til FASTA-filen i /storage
    created_at  TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE genomic_results (
    id           UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    sample_id    UUID REFERENCES genomic_samples(id) ON DELETE CASCADE,
    species_name VARCHAR(200),
    accession    VARCHAR(50),
    identity_pct DECIMAL(5,2),
    score        DECIMAL(10,2),
    ncbi_url     VARCHAR(500),
    raw_result   JSONB,
    created_at   TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_genomic_samples_mission ON genomic_samples(mission_id);
CREATE INDEX idx_genomic_results_sample  ON genomic_results(sample_id);

-- Sample data
INSERT INTO missions (mission_name, mission_description, status, drone_type, location) VALUES
('Bygningsinspeksjon A',  'Inspeksjon av tak og fasade',          'COMPLETED', 'DJI Mavic 3',         'Oslo sentrum'),
('Prøveinnsamling B',     'Biologisk prøveinnsamling i skog',     'ACTIVE',    'Custom Hexacopter',   'Nordmarka'),
('Kartlegging C',         '3D-kartlegging av konstruksjon',       'PLANNED',   'DJI Phantom',         'Fornebu'),
('Overvåking D',          'Overvåking av byggeplass',             'FAILED',    'Parrot Anafi',        'Bærum sentrum'),
('Miljøundersøkelse E',   'Luftkvalitetsmåling i urbane områder', 'COMPLETED', 'DJI Mavic Air 2',     'Grünerløkka, Oslo'),
('Redningsoperasjon F',   'Søk og redning i fjellterreng',        'ACTIVE',    'Custom Octocopter',   'Jotunheimen nasjonalpark');

INSERT INTO detections (mission_id, object_class, confidence, bounding_box) VALUES
(1, 'Person',   0.9876, '{"x": 100, "y": 150, "width": 50,  "height": 100}'),
(2, 'Vehicle',  0.8765, '{"x": 200, "y": 250, "width": 80,  "height": 60}'),
(3, 'Building', 0.7654, '{"x": 300, "y": 350, "width": 120, "height": 200}'),
(4, 'Animal',   0.6543, '{"x": 400, "y": 450, "width": 40,  "height": 80}'),
(5, 'Tree',     0.5432, '{"x": 500, "y": 550, "width": 60,  "height": 150}'),
(6, 'Person',   0.4321, '{"x": 600, "y": 650, "width": 50,  "height": 100}');

INSERT INTO equipment (equipment_id, equipment_name, type, status, drone_compatibility) VALUES
(1, 'High-Res Camera',        'CAMERA',  'IN_USE',      'DJI Mavic 3, DJI Phantom'),
(2, 'Thermal Sensor',         'SENSOR',  'AVAILABLE',   'Custom Hexacopter, Custom Octocopter'),
(3, 'Gripper Arm',            'GRIPPER', 'MAINTENANCE', 'Custom Hexacopter'),
(4, 'LIDAR Scanner',          'SENSOR',  'IN_USE',      'DJI Mavic Air 2, DJI Phantom'),
(5, 'Environmental Sampler',  'SAMPLER', 'AVAILABLE',   'Custom Octocopter');