-- seed.sql


-- Insert administrator user
INSERT INTO users (id, first_name, last_name, email, password, is_admin)
VALUES (
    '36c9050e-ddd3-4c3b-9731-9f487208bbc1',
    'Admin',
    'HBnB',
    'admin@hbnb.io',
    '$2y$12$iK2xy/c.vLgsHXf/hzlOoOH/JkBCkDKkftMa3l.7NJm.aqEAIgLBy',
    TRUE
);

-- Insert initial amenities
INSERT INTO amenities (id, name) VALUES
('70b60c82-594b-4524-a914-657418fb708b', 'WiFi'),
('1aeb848d-c2c6-4f16-bf5e-87a483a22e93', 'Swimming Pool'),
('a5381fb3-dde5-41ad-a9db-86a4107a8542', 'Air Conditioning');