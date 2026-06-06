-- Road Work Ways — Seed Data
-- Run AFTER: alembic upgrade head
-- Provides demo data for local development.

\c roadworks_db

-- ── Users (password = Admin@123, bcrypt hash) ──────────────────────────────
INSERT INTO users (username, email, full_name, password_hash, role, is_active, created_at, updated_at)
VALUES
  ('admin',    'admin@roadworkways.com',    'Administrator',   '$2b$12$N0Mk2O2KVl0cV5zDTKmwwOz.dhxJH1wwNmpF.BO6ICpaxDAaSZ/E6', 'SUPER_ADMIN',     true, NOW(), NOW()),
  ('manager',  'manager@roadworkways.com',  'Project Manager', '$2b$12$N0Mk2O2KVl0cV5zDTKmwwOz.dhxJH1wwNmpF.BO6ICpaxDAaSZ/E6', 'PROJECT_MANAGER', true, NOW(), NOW()),
  ('engineer', 'engineer@roadworkways.com', 'Site Engineer',   '$2b$12$N0Mk2O2KVl0cV5zDTKmwwOz.dhxJH1wwNmpF.BO6ICpaxDAaSZ/E6', 'SITE_ENGINEER',   true, NOW(), NOW())
ON CONFLICT (username) DO NOTHING;

-- ── Vendors ─────────────────────────────────────────────────────────────────
INSERT INTO vendors (vendor_name, contact_person, mobile_number, gst_number, address, created_at, updated_at)
VALUES
  ('Shree Ram Constructions',  'Ramesh Kumar', '9876543210', '29ABCDE1234F1Z5', 'Bangalore, Karnataka', NOW(), NOW()),
  ('National Road Suppliers',  'Suresh Patel', '9988776655', '27FGHIJ5678K2A6', 'Mumbai, Maharashtra',  NOW(), NOW()),
  ('Karnataka Steel & Cement', 'Vijay Rao',    '9871234567', '29KLMNO9012L3B7', 'Mysuru, Karnataka',    NOW(), NOW())
ON CONFLICT (gst_number) DO NOTHING;

-- ── Employees ────────────────────────────────────────────────────────────────
INSERT INTO employees (employee_code, full_name, mobile_number, aadhaar_number, designation, daily_wage, status, joining_date, created_at, updated_at)
VALUES
  ('EMP001', 'Raju Singh',    '9001234567', '123456789012', 'Mason',            650.00, 'ACTIVE', '2023-01-15', NOW(), NOW()),
  ('EMP002', 'Mohan Yadav',   '9012345678', '234567890123', 'Unskilled Labour', 500.00, 'ACTIVE', '2023-02-01', NOW(), NOW()),
  ('EMP003', 'Prem Lal',      '9023456789', '345678901234', 'Helper',           450.00, 'ACTIVE', '2023-03-10', NOW(), NOW()),
  ('EMP004', 'Sunita Devi',   '9034567890', '456789012345', 'Unskilled Labour', 450.00, 'ACTIVE', '2023-04-05', NOW(), NOW()),
  ('EMP005', 'Arjun Thakur',  '9045678901', '567890123456', 'Supervisor',       850.00, 'ACTIVE', '2022-11-20', NOW(), NOW()),
  ('EMP006', 'Kavitha Reddy', '9056789012', '678901234567', 'Mason',            650.00, 'ACTIVE', '2023-05-01', NOW(), NOW())
ON CONFLICT (employee_code) DO NOTHING;

-- ── Projects ─────────────────────────────────────────────────────────────────
INSERT INTO projects (project_code, project_name, location, state, road_type, contract_value, start_date, end_date, status, created_at, updated_at)
VALUES
  ('PROJ001', 'NH-75 Widening Phase 1', 'Hassan to Mangalore', 'Karnataka', 'NATIONAL_HIGHWAY', 28500000.00, '2024-01-15', '2025-06-30', 'IN_PROGRESS', NOW(), NOW()),
  ('PROJ002', 'SH-33 Resurfacing',      'Mysuru Ring Road',    'Karnataka', 'STATE_HIGHWAY',     9800000.00, '2024-03-01', '2024-12-31', 'IN_PROGRESS', NOW(), NOW()),
  ('PROJ003', 'Village Road Koppal',    'Koppal to Yelburga',  'Karnataka', 'RURAL_ROAD',        3200000.00, '2024-06-01', '2024-11-30', 'PLANNING',    NOW(), NOW()),
  ('PROJ004', 'MDR-12 Patch Work',      'Belagavi District',   'Karnataka', 'DISTRICT_ROAD',     4750000.00, '2023-07-01', '2024-01-31', 'COMPLETED',   NOW(), NOW())
ON CONFLICT (project_code) DO NOTHING;

-- ── Materials ────────────────────────────────────────────────────────────────
INSERT INTO materials (material_code, material_name, unit, description, created_at, updated_at)
VALUES
  ('MAT001', 'Bitumen VG30',       'MT',  'Viscosity Grade 30 Bitumen',        NOW(), NOW()),
  ('MAT002', 'Crushed Stone 20mm', 'MT',  '20mm aggregate for road base',      NOW(), NOW()),
  ('MAT003', 'Crushed Stone 40mm', 'MT',  '40mm aggregate for sub-base',       NOW(), NOW()),
  ('MAT004', 'River Sand',         'MT',  'Fine sand for filling',             NOW(), NOW()),
  ('MAT005', 'Cement OPC 53',      'BAG', 'Ordinary Portland Cement 53 grade', NOW(), NOW()),
  ('MAT006', 'Steel TMT 12mm',     'MT',  'TMT bars for RCC work',             NOW(), NOW())
ON CONFLICT (material_code) DO NOTHING;
