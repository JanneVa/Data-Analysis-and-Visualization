-- Consultas SQL para insertar datos en la base de datos
-- Video Streaming Platform

-- Limpiar tablas existentes (opcional)
-- TRUNCATE TABLE viewing_sessions CASCADE;
-- TRUNCATE TABLE content CASCADE;
-- TRUNCATE TABLE users CASCADE;

-- 1. INSERTAR USUARIOS (desde users.csv)
INSERT INTO users (user_id, age, country, subscription_type, registration_date, total_watch_time_hours) VALUES
('U0001', 21, 'Argentina', 'Basic', '2022-10-02', 58.0),
('U0002', 44, 'Mexico', 'Standard', '2022-09-30', 75.3),
('U0003', 20, 'Argentina', 'Standard', '2023-01-24', 360.0),
('U0004', 39, 'Peru', 'Standard', '2022-12-15', 513.0),
('U0005', 25, 'Colombia', 'Premium', '2023-03-10', 245.5),
('U0006', 31, 'Chile', 'Basic', '2022-11-08', 89.2),
('U0007', 28, 'Brazil', 'Premium', '2023-02-14', 678.9),
('U0008', 35, 'Argentina', 'Standard', '2022-08-20', 156.7),
('U0009', 22, 'Mexico', 'Basic', '2023-04-05', 123.4),
('U0010', 29, 'Peru', 'Premium', '2022-12-30', 456.8);

-- 2. INSERTAR CONTENIDO - PELÍCULAS (desde content.json movies)
INSERT INTO content (content_id, title, genre, content_type, duration_minutes, release_year, rating, views_count, production_budget, seasons, episodes_per_season, avg_episode_duration) VALUES
('M001', 'Advanced World', '["Sci-Fi", "Horror", "Drama"]', 'movie', 179, 2020, 3.5, 66721, 220088717, NULL, NULL, NULL),
('M002', 'Neural Signal', '["Sci-Fi", "Thriller"]', 'movie', 142, 2021, 4.2, 54320, 185000000, NULL, NULL, NULL),
('M003', 'Data Dreams', '["Drama", "Technology"]', 'movie', 128, 2022, 4.0, 78945, 150000000, NULL, NULL, NULL),
('M004', 'Quantum Quest', '["Sci-Fi", "Adventure"]', 'movie', 165, 2023, 4.5, 92340, 200000000, NULL, NULL, NULL),
('M005', 'Analytics Academy', '["Drama", "Education"]', 'movie', 95, 2021, 3.8, 45670, 120000000, NULL, NULL, NULL);

-- 3. INSERTAR CONTENIDO - SERIES (desde content.json series)
INSERT INTO content (content_id, title, genre, content_type, duration_minutes, release_year, rating, views_count, production_budget, seasons, episodes_per_season, avg_episode_duration) VALUES
('S001', 'Analytics Chronicles', '["Drama", "Technology"]', 'series', 45, NULL, 4.7, 89650, 120000000, 3, '[10, 12, 8]', 45),
('S002', 'Data Detectives', '["Crime", "Mystery"]', 'series', 52, NULL, 4.3, 67420, 85000000, 2, '[8, 10]', 52),
('S003', 'Machine Learning Masters', '["Drama", "Education"]', 'series', 40, NULL, 4.1, 54320, 95000000, 2, '[12, 10]', 40),
('S004', 'Big Data Brothers', '["Comedy", "Technology"]', 'series', 30, NULL, 3.9, 45670, 70000000, 1, '[15]', 30),
('S005', 'AI Adventures', '["Sci-Fi", "Adventure"]', 'series', 50, NULL, 4.6, 78920, 110000000, 2, '[10, 12]', 50);

-- 4. INSERTAR SESIONES DE VISUALIZACIÓN (desde viewing_sessions.csv)
INSERT INTO viewing_sessions (session_id, user_id, content_id, watch_date, watch_duration_minutes, completion_percentage, device_type, quality_level) VALUES
('S000001', 'U0001', 'S001', '2024-02-16', 9, 18.8, 'Desktop', '4K'),
('S000002', 'U0001', 'M110', '2024-08-06', 30, 23.6, 'Smart TV', 'SD'),
('S000003', 'U0001', 'S005', '2024-03-20', 18, 65.3, 'Desktop', '4K'),
('S000004', 'U0001', 'M105', '2024-02-24', 77, 74.4, 'Mobile', 'HD'),
('S000005', 'U0002', 'M001', '2024-01-15', 45, 25.1, 'Tablet', 'HD'),
('S000006', 'U0002', 'S002', '2024-03-10', 52, 100.0, 'Smart TV', '4K'),
('S000007', 'U0002', 'M003', '2024-02-28', 38, 29.7, 'Desktop', 'HD'),
('S000008', 'U0003', 'S001', '2024-04-05', 45, 100.0, 'Mobile', 'HD'),
('S000009', 'U0003', 'M002', '2024-03-22', 60, 42.3, 'Smart TV', '4K'),
('S000010', 'U0003', 'S003', '2024-04-12', 25, 62.5, 'Tablet', 'SD'),
('S000011', 'U0004', 'M004', '2024-01-30', 90, 54.5, 'Desktop', '4K'),
('S000012', 'U0004', 'S004', '2024-02-15', 30, 100.0, 'Mobile', 'HD'),
('S000013', 'U0005', 'M005', '2024-03-05', 35, 36.8, 'Smart TV', 'HD'),
('S000014', 'U0005', 'S005', '2024-04-01', 50, 100.0, 'Desktop', '4K'),
('S000015', 'U0006', 'M001', '2024-02-20', 40, 22.3, 'Mobile', 'SD'),
('S000016', 'U0006', 'S002', '2024-03-15', 26, 50.0, 'Tablet', 'HD'),
('S000017', 'U0007', 'M003', '2024-01-25', 55, 43.0, 'Smart TV', '4K'),
('S000018', 'U0007', 'S001', '2024-04-08', 45, 100.0, 'Desktop', 'HD'),
('S000019', 'U0008', 'M002', '2024-02-10', 50, 35.2, 'Mobile', 'HD'),
('S000020', 'U0008', 'S003', '2024-03-25', 20, 50.0, 'Tablet', 'SD');

-- 5. CONSULTAS DE VERIFICACIÓN
-- Verificar usuarios insertados
SELECT COUNT(*) as total_users FROM users;

-- Verificar contenido insertado
SELECT content_type, COUNT(*) as count FROM content GROUP BY content_type;

-- Verificar sesiones insertadas
SELECT COUNT(*) as total_sessions FROM viewing_sessions;

-- Verificar integridad referencial
SELECT 
    'Sessions without valid user' as check_type,
    COUNT(*) as count
FROM viewing_sessions vs 
LEFT JOIN users u ON vs.user_id = u.user_id 
WHERE u.user_id IS NULL

UNION ALL

SELECT 
    'Sessions without valid content' as check_type,
    COUNT(*) as count
FROM viewing_sessions vs 
LEFT JOIN content c ON vs.content_id = c.content_id 
WHERE c.content_id IS NULL;

-- 6. CONSULTA DE RESUMEN
SELECT 
    'DATABASE SUMMARY' as summary_type,
    (SELECT COUNT(*) FROM users) as users_count,
    (SELECT COUNT(*) FROM content WHERE content_type = 'movie') as movies_count,
    (SELECT COUNT(*) FROM content WHERE content_type = 'series') as series_count,
    (SELECT COUNT(*) FROM viewing_sessions) as sessions_count;
