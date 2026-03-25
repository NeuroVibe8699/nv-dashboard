-- =========================================================
-- NeuroVibe AI Technologies - NV-8699 System Database
-- =========================================================

-- Pehle purane tables ko hata dete hain (Fresh Start ke liye)
DROP TABLE IF EXISTS sensor_data CASCADE;
DROP TABLE IF EXISTS inventory CASCADE;
DROP TABLE IF EXISTS users CASCADE;

-- 1. USER MANAGEMENT TABLE
-- Role based access: 'admin' for full control, 'client' for dashboard only
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    username VARCHAR(100) UNIQUE NOT NULL,
    password_hash TEXT NOT NULL,
    role VARCHAR(20) DEFAULT 'client' CHECK (role IN ('admin', 'client')),
    company_name VARCHAR(150) DEFAULT 'NeuroVibe AI Technologies',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 2. GATEWAY INVENTORY TABLE
-- Provisioning and tracking for i.MX6 Gateways
CREATE TABLE inventory (
    id SERIAL PRIMARY KEY,
    gateway_id VARCHAR(50) UNIQUE NOT NULL, -- e.g., GW_8699
    status VARCHAR(20) DEFAULT 'active',
    firmware_version VARCHAR(20) DEFAULT 'v1.0.0',
    last_ping TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 3. SENSOR DATA TABLE (RAW & CALCULATED)
-- Backend calculations for RPM, Velocity, and Vibration (g)
CREATE TABLE sensor_data (
    id SERIAL PRIMARY KEY,
    gateway_id VARCHAR(50) REFERENCES inventory(gateway_id),
    rpm FLOAT DEFAULT 0.0,
    velocity FLOAT DEFAULT 0.0,
    vibration_g FLOAT DEFAULT 0.0,
    ultrasound_db FLOAT DEFAULT 0.0,
    flux FLOAT DEFAULT 0.0,
    temperature FLOAT DEFAULT 0.0,
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- =========================================================
-- DEFAULT SEED DATA (Login Credentials)
-- =========================================================

-- Note: Passwords are 'admin123' and 'client123' (Flask hash formatted)

-- 1. Insert Admin User
INSERT INTO users (username, password_hash, role, company_name) 
VALUES (
    'admin@nvpredictive.com', 
    'pbkdf2:sha256:260000$admin123', 
    'admin', 
    'NeuroVibe Admin'
);

-- 2. Insert Client User
INSERT INTO users (username, password_hash, role, company_name) 
VALUES (
    'client@nvpredictive.com', 
    'pbkdf2:sha256:260000$client123', 
    'client', 
    'NeuroVibe Client'
);

-- 3. Provision First Gateway
INSERT INTO inventory (gateway_id, status, firmware_version) 
VALUES ('GW_8699', 'active', 'v1.0.2');

-- =========================================================
-- DATABASE SETUP COMPLETE
-- =========================================================
