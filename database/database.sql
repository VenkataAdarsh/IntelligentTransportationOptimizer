
-- ==========================================
-- INTELLIGENT TRANSPORTATION COST OPTIMIZER
-- DATABASE CREATION
-- ==========================================

CREATE DATABASE IF NOT EXISTS transportation_optimizer;

USE transportation_optimizer;


-- ==========================================
-- 1. VEHICLES TABLE
-- ==========================================

CREATE TABLE IF NOT EXISTS vehicles (
    vehicle_id INT AUTO_INCREMENT PRIMARY KEY,
    vehicle_name VARCHAR(100) NOT NULL,
    vehicle_type VARCHAR(50) NOT NULL,
    capacity INT NOT NULL,
    fuel_cost DECIMAL(10,2) DEFAULT 0,
    status VARCHAR(30) DEFAULT 'Available',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);


-- ==========================================
-- 2. ROUTES TABLE
-- ==========================================

CREATE TABLE IF NOT EXISTS routes (
    route_id INT AUTO_INCREMENT PRIMARY KEY,
    source VARCHAR(100) NOT NULL,
    destination VARCHAR(100) NOT NULL,
    distance DECIMAL(10,2) NOT NULL,
    toll_cost DECIMAL(10,2) DEFAULT 0,
    fuel_cost DECIMAL(10,2) DEFAULT 0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);


-- ==========================================
-- 3. OPTIMIZATION HISTORY TABLE
-- ==========================================

CREATE TABLE IF NOT EXISTS optimization_history (
    optimization_id INT AUTO_INCREMENT PRIMARY KEY,
    total_cost DECIMAL(12,2) NOT NULL,
    total_quantity INT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);


-- ==========================================
-- 4. TRANSPORTATION RESULTS TABLE
-- ==========================================

CREATE TABLE IF NOT EXISTS transportation_results (
    result_id INT AUTO_INCREMENT PRIMARY KEY,
    optimization_id INT NOT NULL,
    source VARCHAR(100) NOT NULL,
    destination VARCHAR(100) NOT NULL,
    allocated_quantity INT NOT NULL,
    unit_cost DECIMAL(10,2) NOT NULL,
    total_cost DECIMAL(12,2) NOT NULL,

    FOREIGN KEY (optimization_id)
    REFERENCES optimization_history(optimization_id)
    ON DELETE CASCADE
);


-- ==========================================
-- 5. SAMPLE VEHICLE DATA
-- ==========================================

INSERT INTO vehicles
(vehicle_name, vehicle_type, capacity, fuel_cost)
VALUES
('Truck 01', 'Heavy Truck', 100, 15.50),
('Truck 02', 'Medium Truck', 70, 12.00),
('Van 01', 'Delivery Van', 30, 9.50);


-- ==========================================
-- 6. SAMPLE ROUTE DATA
-- ==========================================

INSERT INTO routes
(source, destination, distance, toll_cost, fuel_cost)
VALUES
('Bengaluru', 'Mysuru', 145, 100, 800),
('Bengaluru', 'Hubballi', 410, 250, 2200),
('Bengaluru', 'Mangaluru', 350, 180, 1900);


-- ==========================================
-- END OF DATABASE SCRIPT
-- ==========================================

SELECT * FROM vehicles;

SELECT * FROM routes;

SELECT * FROM optimization_history;
