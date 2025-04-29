    -- Sample data for WaveExpress ticketing system

-- Destinations
INSERT INTO reservations_destination (name, description) VALUES 
('Boracay', 'Famous for its pristine white sand beaches and crystal-clear waters.'),
('Palawan', 'Known for its limestone cliffs, lagoons, and beautiful beaches.'),
('Cebu', 'A vibrant city with historical landmarks and beautiful islands.'),
('Bohol', 'Home to the Chocolate Hills and tarsiers.'),
('Siargao', 'Known as the surfing capital of the Philippines.');

-- Schedules
-- Manila to Boracay
INSERT INTO reservations_schedule (origin, destination_id, departure_date, departure_time, price, available_seats) VALUES 
('Manila', 1, CURDATE(), '08:00:00', 1500.00, 50),
('Manila', 1, CURDATE(), '13:00:00', 1500.00, 50),
('Manila', 1, CURDATE() + INTERVAL 1 DAY, '08:00:00', 1500.00, 50),
('Manila', 1, CURDATE() + INTERVAL 1 DAY, '13:00:00', 1500.00, 50);

-- Cebu to Bohol
INSERT INTO reservations_schedule (origin, destination_id, departure_date, departure_time, price, available_seats) VALUES 
('Cebu', 4, CURDATE(), '09:00:00', 800.00, 50),
('Cebu', 4, CURDATE(), '14:00:00', 800.00, 50),
('Cebu', 4, CURDATE() + INTERVAL 1 DAY, '09:00:00', 800.00, 50),
('Cebu', 4, CURDATE() + INTERVAL 1 DAY, '14:00:00', 800.00, 50);

-- Batangas to Puerto Galera
INSERT INTO reservations_schedule (origin, destination_id, departure_date, departure_time, price, available_seats) VALUES 
('Batangas', 3, CURDATE(), '10:00:00', 350.00, 50),
('Batangas', 3, CURDATE(), '15:00:00', 350.00, 50),
('Batangas', 3, CURDATE() + INTERVAL 1 DAY, '10:00:00', 350.00, 50),
('Batangas', 3, CURDATE() + INTERVAL 1 DAY, '15:00:00', 350.00, 50);

-- Manila to Palawan
INSERT INTO reservations_schedule (origin, destination_id, departure_date, departure_time, price, available_seats) VALUES 
('Manila', 2, CURDATE(), '07:00:00', 1200.00, 50),
('Manila', 2, CURDATE() + INTERVAL 1 DAY, '07:00:00', 1200.00, 50);

-- Manila to Siargao
INSERT INTO reservations_schedule (origin, destination_id, departure_date, departure_time, price, available_seats) VALUES 
('Manila', 5, CURDATE(), '06:00:00', 1800.00, 50),
('Manila', 5, CURDATE() + INTERVAL 2 DAY, '06:00:00', 1800.00, 50);

-- Create stored procedure for finding available schedules
DELIMITER //
CREATE PROCEDURE IF NOT EXISTS FindAvailableSchedules(
    IN p_origin VARCHAR(100),
    IN p_destination VARCHAR(100),
    IN p_departure_date DATE,
    IN p_passengers INT
)
BEGIN
    SELECT s.id, s.origin, d.name as destination_name, 
           s.departure_date, s.departure_time, s.price, s.available_seats
    FROM reservations_schedule s
    JOIN reservations_destination d ON s.destination_id = d.id
    WHERE s.origin LIKE CONCAT('%', p_origin, '%')
    AND d.name LIKE CONCAT('%', p_destination, '%')
    AND s.departure_date = p_departure_date
    AND s.available_seats >= p_passengers;
END //
DELIMITER ;
