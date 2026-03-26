-- =========================================================
-- NEUROVIBE AI TECHNOLOGIES PVT LTD - MASTER GLOBAL SCHEMA
-- Optimized for: EFM32/MSP432 Nodes (NVS-1001 to 1010) 
-- & i.MX6 Gateways (NV-1001/1002)
-- =========================================================

-- 1. USER & CLIENT ACCESS
CREATE TABLE IF NOT EXISTS users (
    id SERIAL PRIMARY KEY,
    username VARCHAR(100) UNIQUE NOT NULL,
    password_hash TEXT NOT NULL,
    role VARCHAR(20) DEFAULT 'client' CHECK (role IN ('admin', 'client')),
    email VARCHAR(150) UNIQUE NOT NULL,
    whatsapp_no VARCHAR(20),
    company_name VARCHAR(150) DEFAULT 'NeuroVibe AI Technologies Pvt Ltd',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 2. GLOBAL DEVICE INVENTORY (For Bulk Excel Import)
-- Centralized tracking for Radio MAC (Node) and IMEI (Gateway)
CREATE TABLE IF NOT EXISTS device_inventory (
    id SERIAL PRIMARY KEY,
    model_id VARCHAR(20) NOT NULL,      -- NV-1001/1002 or NVS-1001 to 1010
    serial_no VARCHAR(50) UNIQUE NOT NULL,
    radio_mac VARCHAR(50) UNIQUE,       -- PRIMARY ID FOR NODES
    imei_id VARCHAR(50) UNIQUE,         -- PRIMARY ID FOR GATEWAYS
    ble_mac VARCHAR(50),
    lan_mac VARCHAR(50),
    wan_mac VARCHAR(50),
    rf_frequency INT NOT NULL,          -- 868 or 915 (Strictly Separate)
    production_batch VARCHAR(50),       -- Batch tracking for quality control
    device_status VARCHAR(20) DEFAULT 'factory_stock', -- [factory_stock, deployed, active]
    registration_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 3. SITE MAPPING & RCP MATRIX (The Machine Profile)
-- Maps a specific Node to a User's Machine/Site and sets AI Thresholds
CREATE TABLE IF NOT EXISTS site_node_mapping (
    id SERIAL PRIMARY KEY,
    user_id INT REFERENCES users(id) ON DELETE CASCADE,
    radio_mac VARCHAR(50) REFERENCES device_inventory(radio_mac) ON DELETE CASCADE,
    site_name VARCHAR(200) NOT NULL,     -- e.g., 'Ammonia Pump Site A'
    motor_kw FLOAT,                     -- Motor Power for AI Scaling
    rated_rpm INT,                      -- For RPM Calculation logic
    vib_limit_mm_s FLOAT DEFAULT 4.5,   -- ISO 10816 Standard Alert Limit
    overall_interval_min INT DEFAULT 15, -- Scheduling: 5m to 1440m (24h)
    spectrum_interval_hr INT DEFAULT 1,  -- Scheduling: 1h to 24h
    last_sync TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 4. REAL-TIME TELEMETRY (Overall & Spectrum Data)
-- Stores Pick-to-Pick data from Nodes
CREATE TABLE IF NOT EXISTS node_data (
    id SERIAL PRIMARY KEY,
    radio_mac VARCHAR(50) REFERENCES device_inventory(radio_mac),
    velocity FLOAT,          -- Velocity (mm/s)
    acceleration FLOAT,      -- Acceleration (g)
    temperature FLOAT,       -- Temp (C)
    ultrasound_db FLOAT,     -- Acoustic (dB)
    magnetic_flux FLOAT,     -- Flux (Tesla)
    calculated_rpm INT,      -- Computed RPM
    ai_alert_status BOOLEAN DEFAULT FALSE, -- AI-Edge Detection Flag
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Indexes for Ultra-Fast Search during Gateway Handshake
CREATE INDEX IF NOT EXISTS idx_radio_mac ON device_inventory(radio_mac);
CREATE INDEX IF NOT EXISTS idx_imei_id ON device_inventory(imei_id);
