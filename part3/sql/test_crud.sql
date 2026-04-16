-- test_crud.sql
USE hbnb_db;

-- =====================================
-- SELECT: verify seeded data
-- =====================================
SELECT * FROM users;
SELECT * FROM amenities;

-- =====================================
-- INSERT: create a normal user
-- =====================================
INSERT INTO users (id, first_name, last_name, email, password, is_admin)
VALUES (
    '4ff49cea-136a-44c0-8c91-e9a3d1ff2409',
    'Lara',
    'Z',
    'lara@example.com',
    '$2y$12$iK2xy/c.vLgsHXf/hzlOoOH/JkBCkDKkftMa3l.7NJm.aqEAIgLBy',
    FALSE
);

-- INSERT: create a place owned by Lara
INSERT INTO places (id, title, description, price, latitude, longitude, owner_id)
VALUES (
    'bb4b67d2-c2d8-40d7-a09a-7f81e14208cb',
    'Nice Flat',
    'A clean and comfortable apartment',
    150.00,
    24.7136,
    46.6753,
    '4ff49cea-136a-44c0-8c91-e9a3d1ff2409'
);

-- INSERT: connect amenities to place
INSERT INTO place_amenity (place_id, amenity_id) VALUES
('bb4b67d2-c2d8-40d7-a09a-7f81e14208cb', '70b60c82-594b-4524-a914-657418fb708b'),
('bb4b67d2-c2d8-40d7-a09a-7f81e14208cb', 'a5381fb3-dde5-41ad-a9db-86a4107a8542');

-- INSERT: create a review
INSERT INTO reviews (id, text, rating, user_id, place_id)
VALUES (
    'a6fb2a22-fd34-4dd8-bb5c-a7c4b3dfb199',
    'Very nice place and clean.',
    5,
    '4ff49cea-136a-44c0-8c91-e9a3d1ff2409',
    'bb4b67d2-c2d8-40d7-a09a-7f81e14208cb'
);

-- =====================================
-- SELECT: verify relationships
-- =====================================
SELECT * FROM places;
SELECT * FROM reviews;
SELECT * FROM place_amenity;

-- Join query: place with owner
SELECT
    p.id,
    p.title,
    p.price,
    u.first_name,
    u.last_name,
    u.email
FROM places p
JOIN users u ON p.owner_id = u.id;

-- Join query: place amenities
SELECT
    p.title,
    a.name AS amenity_name
FROM place_amenity pa
JOIN places p ON pa.place_id = p.id
JOIN amenities a ON pa.amenity_id = a.id
WHERE p.id = 'bb4b67d2-c2d8-40d7-a09a-7f81e14208cb';

-- Join query: reviews with user and place
SELECT
    r.id,
    r.text,
    r.rating,
    u.email AS reviewer,
    p.title AS place_title
FROM reviews r
JOIN users u ON r.user_id = u.id
JOIN places p ON r.place_id = p.id;

-- =====================================
-- UPDATE tests
-- =====================================
UPDATE places
SET price = 175.00
WHERE id = 'bb4b67d2-c2d8-40d7-a09a-7f81e14208cb';

UPDATE reviews
SET text = 'Updated review: still an excellent place.',
    rating = 4
WHERE id = 'a6fb2a22-fd34-4dd8-bb5c-a7c4b3dfb199';

SELECT * FROM places WHERE id = 'bb4b67d2-c2d8-40d7-a09a-7f81e14208cb';
SELECT * FROM reviews WHERE id = 'a6fb2a22-fd34-4dd8-bb5c-a7c4b3dfb199';

-- =====================================
-- DELETE tests
-- =====================================
DELETE FROM reviews
WHERE id = 'a6fb2a22-fd34-4dd8-bb5c-a7c4b3dfb199';

SELECT * FROM reviews;

-- Optional cleanup
DELETE FROM place_amenity
WHERE place_id = 'bb4b67d2-c2d8-40d7-a09a-7f81e14208cb';

DELETE FROM places
WHERE id = 'bb4b67d2-c2d8-40d7-a09a-7f81e14208cb';

DELETE FROM users
WHERE id = '4ff49cea-136a-44c0-8c91-e9a3d1ff2409';

SELECT * FROM users;
SELECT * FROM places;
SELECT * FROM place_amenity;