-- Video Streaming Platform Database Schema (updated for movies and series)
-- PostgreSQL Implementation

-- Note: Create database outside if needed: CREATE DATABASE video_streaming_platform;
-- Use: \c video_streaming_platform;

CREATE TABLE IF NOT EXISTS users (
	user_id VARCHAR(20) PRIMARY KEY,
	age INTEGER,
	country VARCHAR(100),
	subscription_type VARCHAR(50),
	registration_date DATE,
	total_watch_time_hours DECIMAL(10,2),
	
);

-- Content table (unified for movies and series)
CREATE TABLE IF NOT EXISTS content (
	content_id VARCHAR(20) PRIMARY KEY,
	title VARCHAR(255) NOT NULL,
	genre JSONB, -- array of strings
	content_type VARCHAR(20) NOT NULL, -- 'movie' or 'series'
	duration_minutes INTEGER, -- for movies, avg_episode_duration for series
	release_year INTEGER,
	rating DECIMAL(3,1),
	views_count INTEGER, -- total_views for series
	production_budget BIGINT,
	-- Series-specific fields (NULL for movies)
	seasons INTEGER,
	episodes_per_season JSONB, -- array of integers
	avg_episode_duration INTEGER, -- for series
	
);

CREATE TABLE IF NOT EXISTS viewing_sessions (
	session_id VARCHAR(20) PRIMARY KEY,
	user_id VARCHAR(20) REFERENCES users(user_id),
	content_id VARCHAR(20) REFERENCES content(content_id),
	watch_date DATE NOT NULL,
	watch_duration_minutes INTEGER,
	completion_percentage DECIMAL(5,2),
	device_type VARCHAR(50),
	quality_level VARCHAR(20),
	
);

-- Helpful indexes
CREATE INDEX IF NOT EXISTS idx_users_country ON users(country);
CREATE INDEX IF NOT EXISTS idx_users_subscription_type ON users(subscription_type);
CREATE INDEX IF NOT EXISTS idx_content_type ON content(content_type);
CREATE INDEX IF NOT EXISTS idx_content_release_year ON content(release_year);
CREATE INDEX IF NOT EXISTS idx_sessions_user ON viewing_sessions(user_id);
CREATE INDEX IF NOT EXISTS idx_sessions_content ON viewing_sessions(content_id);
CREATE INDEX IF NOT EXISTS idx_sessions_date ON viewing_sessions(watch_date);

-- Views for quick analysis
CREATE OR REPLACE VIEW user_engagement_summary AS
SELECT 
	u.user_id,
	u.country,
	u.subscription_type,
	COUNT(v.session_id) AS total_sessions,
	COALESCE(SUM(v.watch_duration_minutes),0) AS total_watch_minutes,
	AVG(v.completion_percentage) AS avg_completion_percentage
FROM users u
LEFT JOIN viewing_sessions v ON v.user_id = u.user_id
GROUP BY u.user_id, u.country, u.subscription_type;

CREATE OR REPLACE VIEW content_performance_summary AS
SELECT 
	c.content_id,
	c.title,
	c.content_type,
	c.release_year,
	c.rating,
	COUNT(v.session_id) AS total_views,
	AVG(v.completion_percentage) AS avg_completion_percentage,
	AVG(v.watch_duration_minutes) AS avg_watch_duration
FROM content c
LEFT JOIN viewing_sessions v ON v.content_id = c.content_id
GROUP BY c.content_id, c.title, c.content_type, c.release_year, c.rating;

-- View for movies vs series comparison
CREATE OR REPLACE VIEW content_type_analysis AS
SELECT 
	c.content_type,
	COUNT(*) as content_count,
	AVG(c.rating) as avg_rating,
	AVG(c.views_count) as avg_views,
	AVG(c.production_budget) as avg_budget,
	AVG(v.completion_percentage) as avg_completion_rate
FROM content c
LEFT JOIN viewing_sessions v ON c.content_id = v.content_id
GROUP BY c.content_type;
