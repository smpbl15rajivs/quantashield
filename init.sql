-- QuantaShield Database Initialization Script

-- Create database if not exists (handled by Docker environment)
-- CREATE DATABASE IF NOT EXISTS quantashield;

-- Use the quantashield database
\c quantashield;

-- Create users table
CREATE TABLE IF NOT EXISTS users (
    id SERIAL PRIMARY KEY,
    username VARCHAR(100) UNIQUE NOT NULL,
    email VARCHAR(255) UNIQUE NOT NULL,
    password_hash VARCHAR(255),
    oauth_provider VARCHAR(50),
    oauth_id VARCHAR(255),
    first_name VARCHAR(100),
    last_name VARCHAR(100),
    is_active BOOLEAN DEFAULT TRUE,
    is_admin BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    last_login TIMESTAMP
);

-- Create sessions table
CREATE TABLE IF NOT EXISTS sessions (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(id) ON DELETE CASCADE,
    session_token VARCHAR(255) UNIQUE NOT NULL,
    expires_at TIMESTAMP NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    ip_address INET,
    user_agent TEXT
);

-- Create threats table
CREATE TABLE IF NOT EXISTS threats (
    id SERIAL PRIMARY KEY,
    threat_type VARCHAR(100) NOT NULL,
    severity VARCHAR(20) NOT NULL CHECK (severity IN ('low', 'medium', 'high', 'critical')),
    title VARCHAR(255) NOT NULL,
    description TEXT,
    source VARCHAR(100),
    indicators JSONB,
    status VARCHAR(20) DEFAULT 'active' CHECK (status IN ('active', 'resolved', 'investigating')),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    resolved_at TIMESTAMP
);

-- Create assets table
CREATE TABLE IF NOT EXISTS assets (
    id SERIAL PRIMARY KEY,
    asset_type VARCHAR(100) NOT NULL,
    name VARCHAR(255) NOT NULL,
    ip_address INET,
    hostname VARCHAR(255),
    os VARCHAR(100),
    version VARCHAR(100),
    status VARCHAR(20) DEFAULT 'active' CHECK (status IN ('active', 'inactive', 'maintenance')),
    risk_score INTEGER DEFAULT 0 CHECK (risk_score >= 0 AND risk_score <= 100),
    last_scan TIMESTAMP,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Create incidents table
CREATE TABLE IF NOT EXISTS incidents (
    id SERIAL PRIMARY KEY,
    title VARCHAR(255) NOT NULL,
    description TEXT,
    severity VARCHAR(20) NOT NULL CHECK (severity IN ('low', 'medium', 'high', 'critical')),
    status VARCHAR(20) DEFAULT 'open' CHECK (status IN ('open', 'investigating', 'resolved', 'closed')),
    assigned_to INTEGER REFERENCES users(id),
    created_by INTEGER REFERENCES users(id),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    resolved_at TIMESTAMP
);

-- Create audit_logs table
CREATE TABLE IF NOT EXISTS audit_logs (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(id),
    action VARCHAR(100) NOT NULL,
    resource_type VARCHAR(100),
    resource_id INTEGER,
    details JSONB,
    ip_address INET,
    user_agent TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Create indexes for better performance
CREATE INDEX IF NOT EXISTS idx_users_email ON users(email);
CREATE INDEX IF NOT EXISTS idx_users_username ON users(username);
CREATE INDEX IF NOT EXISTS idx_sessions_token ON sessions(session_token);
CREATE INDEX IF NOT EXISTS idx_sessions_user_id ON sessions(user_id);
CREATE INDEX IF NOT EXISTS idx_threats_severity ON threats(severity);
CREATE INDEX IF NOT EXISTS idx_threats_status ON threats(status);
CREATE INDEX IF NOT EXISTS idx_assets_status ON assets(status);
CREATE INDEX IF NOT EXISTS idx_incidents_status ON incidents(status);
CREATE INDEX IF NOT EXISTS idx_incidents_severity ON incidents(severity);
CREATE INDEX IF NOT EXISTS idx_audit_logs_user_id ON audit_logs(user_id);
CREATE INDEX IF NOT EXISTS idx_audit_logs_created_at ON audit_logs(created_at);

-- Insert default admin user
INSERT INTO users (username, email, password_hash, first_name, last_name, is_admin, is_active)
VALUES (
    'admin',
    'admin@quantashield.in',
    '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewdBPj3QJb9m/NG2', -- password: 'password'
    'Admin',
    'User',
    TRUE,
    TRUE
) ON CONFLICT (username) DO NOTHING;

-- Insert sample threat data
INSERT INTO threats (threat_type, severity, title, description, source, status)
VALUES 
    ('malware', 'high', 'Suspicious File Detected', 'Potential malware detected in system files', 'antivirus', 'active'),
    ('network', 'medium', 'Unusual Network Traffic', 'Abnormal outbound connections detected', 'firewall', 'investigating'),
    ('phishing', 'critical', 'Phishing Email Campaign', 'Large-scale phishing campaign targeting employees', 'email_security', 'active')
ON CONFLICT DO NOTHING;

-- Insert sample asset data
INSERT INTO assets (asset_type, name, ip_address, hostname, os, status, risk_score)
VALUES 
    ('server', 'Web Server 01', '192.168.1.10', 'web01.quantashield.in', 'Ubuntu 24.04', 'active', 25),
    ('server', 'Database Server', '192.168.1.20', 'db01.quantashield.in', 'Ubuntu 24.04', 'active', 15),
    ('workstation', 'Admin Workstation', '192.168.1.100', 'admin-ws.quantashield.in', 'Windows 11', 'active', 35)
ON CONFLICT DO NOTHING;

-- Insert sample incident data
INSERT INTO incidents (title, description, severity, status, created_by)
VALUES 
    ('Security Breach Investigation', 'Investigating potential unauthorized access to system', 'high', 'investigating', 1),
    ('Malware Cleanup', 'Cleaning infected workstation', 'medium', 'open', 1),
    ('Policy Violation', 'User accessed restricted resources', 'low', 'resolved', 1)
ON CONFLICT DO NOTHING;

-- Create trigger to update updated_at timestamp
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = CURRENT_TIMESTAMP;
    RETURN NEW;
END;
$$ language 'plpgsql';

-- Apply triggers to tables with updated_at columns
CREATE TRIGGER update_users_updated_at BEFORE UPDATE ON users FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();
CREATE TRIGGER update_threats_updated_at BEFORE UPDATE ON threats FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();
CREATE TRIGGER update_assets_updated_at BEFORE UPDATE ON assets FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();
CREATE TRIGGER update_incidents_updated_at BEFORE UPDATE ON incidents FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

-- Grant permissions
GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public TO quantashield;
GRANT ALL PRIVILEGES ON ALL SEQUENCES IN SCHEMA public TO quantashield;

