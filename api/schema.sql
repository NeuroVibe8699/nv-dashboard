-- =========================================================
-- NeuroVibe AI Technologies - Professional Master Schema
-- =========================================================

-- 1. USER MANAGEMENT (Admin & Clients)
CREATE TABLE IF NOT EXISTS users (
    id SERIAL PRIMARY KEY,
    username VARCHAR(100) UNIQUE NOT NULL,
    password_hash TEXT NOT NULL,
    role VARCHAR(20) DEFAULT 'client' CHECK (role IN ('admin', 'client')),
    email VARCHAR(150) UNIQUE,
    whatsapp_no VARCHAR(20),
    company_name VARCHAR(150) DEFAULT 'NeuroVibe AI Technologies',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 2. GLOBAL INVENTORY (Gateways & Nodes)
-- Covers Models NV-1001, NV-1002 and NVS-1001 to NVS-1010
CREATE TABLE IF NOT EXISTS inventory (
    id SERIAL PRIMARY KEY,
    model_no VARCHAR(20) NOT NULL, -- e.g., NV-1001, NVS-1010
    serial_no VARCHAR(100) UNIQUE NOT NULL,
    imei VARCHAR(50),               -- Gateway ID (Primary)
    radio_mac VARCHAR(50) UNIQUE,    -- Node ID (Primary)
    ble_mac VARCHAR(50),
    lan_mac VARCHAR(50),
    wan_mac VARCHAR(50),
    region_freq VARCHAR(10),        -- 868MHz / 915MHz
    status VARCHAR(20) DEFAULT 'unassigned', -- unassigned, active, maintenance
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 3. SITE & NODE CONFIGURATION (The RCP Matrix)
-- Mapping every Node to a specific Machine/Site and its AI Thresholds
CREATE TABLE IF NOT EXISTS node_configs (
    id SERIAL PRIMARY KEY,
    user_id INT REFERENCES users(id) ON DELETE CASCADE,
    node_id VARCHAR(50) REFERENCES inventory(radio_mac) ON DELETE CASCADE,
    site_name VARCHAR(200) NOT NULL, -- e.g., Ammonia Pump 01
    motor_capacity_kw FLOAT,        -- Motor Power
    rated_rpm INT,                  -- e.g., 1440
    vibration_threshold_mm_s FLOAT DEFAULT 4.5, -- AI Alert Limit
    temp_threshold_c FLOAT DEFAULT 55.0,         -- AI Alert Limit
    overall_interval_sec INT DEFAULT 300,        -- 5 min to 24h
    spectrum_interval_sec INT DEFAULT 3600,      -- 1h to 24h
    last_calibrated TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 4. LIVE SENSOR DATA (Pick-to-Pick Storage)
CREATE TABLE IF NOT EXISTS sensor_data (
    id SERIAL PRIMARY KEY,
    node_id VARCHAR(50) REFERENCES inventory(radio_mac) ON DELETE CASCADE,
    velocity FLOAT,
    acceleration FLOAT,
    temperature FLOAT,
    flux FLOAT,
    rpm INT,
    ultrasound_db FLOAT,
    is_ai_alert BOOLEAN DEFAULT FALSE,
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- =========================================================
-- DEFAULT SEED DATA (First Time Setup)
-- =========================================================

-- Admin Login: admin@nvpredictive.com / admin123
INSERT INTO users (username, password_hash, role, email, company_name) 
VALUES (
    'admin@nvpredictive.com', 
    'pbkdf2:sha256:260000$admin123', 
    'admin', 
    'admin@nvpredictive.com', 
    'NeuroVibe Master Admin'
) ON CONFLICT DO NOTHING;

-- Initial Model Provisioning Example (NVS-1010 AI Node)
INSERT INTO inventory (model_no, serial_no, radio_mac, region_freq, status) 
VALUES ('NVS-1010', 'SN-8699-001', 'AA:BB:CC:DD:EE:FF', '868MHz', 'unassigned') 
ON CONFLICT DO NOTHING;

-- =========================================================
-- DATABASE SETUP COMPLETE
-- =========================================================

