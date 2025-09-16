-- Complex Analytical Queries for Video Streaming Platform

-- 1. User Engagement Analysis by Subscription Tier
WITH user_metrics AS (
    SELECT 
        u.user_id,
        u.subscription_type,
        u.country,
        COUNT(vs.session_id) as session_count,
        SUM(vs.watch_duration_minutes) as total_watch_minutes,
        AVG(vs.completion_percentage) as avg_completion,
        COUNT(DISTINCT vs.content_id) as unique_content_watched,
        MAX(vs.watch_date) as last_watch_date
    FROM users u
    LEFT JOIN viewing_sessions vs ON u.user_id = vs.user_id
    GROUP BY u.user_id, u.subscription_type, u.country
),
subscription_analysis AS (
    SELECT 
        subscription_type,
        COUNT(*) as user_count,
        AVG(session_count) as avg_sessions_per_user,
        AVG(total_watch_minutes) as avg_watch_minutes,
        AVG(avg_completion) as avg_completion_rate,
        AVG(unique_content_watched) as avg_unique_content,
        PERCENTILE_CONT(0.5) WITHIN GROUP (ORDER BY session_count) as median_sessions
    FROM user_metrics
    GROUP BY subscription_type
)
SELECT * FROM subscription_analysis
ORDER BY avg_watch_minutes DESC;

-- 2. Content Performance Analysis with Quality Metrics
WITH content_metrics AS (
    SELECT 
        c.content_id,
        c.title,
        c.genre,
        c.duration_minutes,
        c.release_year,
        c.rating,
        COUNT(vs.session_id) as total_views,
        AVG(vs.completion_percentage) as avg_completion,
        AVG(vs.watch_duration_minutes) as avg_watch_duration,
        COUNT(DISTINCT vs.user_id) as unique_viewers,
        SUM(CASE WHEN vs.quality_level = '4K' THEN 1 ELSE 0 END) as hd_views,
        SUM(CASE WHEN vs.quality_level IN ('HD', '4K') THEN 1 ELSE 0 END) as high_quality_views
    FROM content c
    LEFT JOIN viewing_sessions vs ON c.content_id = vs.content_id
    GROUP BY c.content_id, c.title, c.genre, c.duration_minutes, c.release_year, c.rating
)
SELECT 
    *,
    ROUND((high_quality_views::DECIMAL / NULLIF(total_views, 0)) * 100, 2) as hq_percentage,
    ROUND((avg_watch_duration::DECIMAL / duration_minutes) * 100, 2) as engagement_rate
FROM content_metrics
WHERE total_views > 0
ORDER BY engagement_rate DESC, total_views DESC;

-- 3. Geographic Performance Analysis
WITH country_metrics AS (
    SELECT 
        u.country,
        COUNT(DISTINCT u.user_id) as total_users,
        COUNT(vs.session_id) as total_sessions,
        AVG(vs.completion_percentage) as avg_completion,
        AVG(vs.watch_duration_minutes) as avg_session_duration,
        SUM(CASE WHEN vs.quality_level IN ('HD', '4K') THEN 1 ELSE 0 END) as hd_sessions,
        COUNT(DISTINCT vs.content_id) as unique_content_watched
    FROM users u
    LEFT JOIN viewing_sessions vs ON u.user_id = vs.user_id
    GROUP BY u.country
)
SELECT 
    *,
    ROUND((hd_sessions::DECIMAL / NULLIF(total_sessions, 0)) * 100, 2) as hd_percentage,
    ROUND(total_sessions::DECIMAL / NULLIF(total_users, 0), 2) as sessions_per_user
FROM country_metrics
WHERE total_users > 0
ORDER BY sessions_per_user DESC;

-- 4. Device and Quality Analysis
SELECT 
    device_type,
    quality_level,
    COUNT(*) as session_count,
    AVG(completion_percentage) as avg_completion,
    AVG(watch_duration_minutes) as avg_duration,
    PERCENTILE_CONT(0.25) WITHIN GROUP (ORDER BY completion_percentage) as q1_completion,
    PERCENTILE_CONT(0.75) WITHIN GROUP (ORDER BY completion_percentage) as q3_completion
FROM viewing_sessions
GROUP BY device_type, quality_level
ORDER BY device_type, quality_level;

-- 5. User Retention Analysis (30-day cohorts)
WITH user_first_watch AS (
    SELECT 
        user_id,
        MIN(watch_date) as first_watch_date
    FROM viewing_sessions
    GROUP BY user_id
),
cohort_analysis AS (
    SELECT 
        DATE_TRUNC('month', ufw.first_watch_date) as cohort_month,
        COUNT(DISTINCT ufw.user_id) as cohort_size,
        COUNT(DISTINCT vs.user_id) as retained_users
    FROM user_first_watch ufw
    LEFT JOIN viewing_sessions vs ON ufw.user_id = vs.user_id 
        AND vs.watch_date >= ufw.first_watch_date + INTERVAL '30 days'
    GROUP BY DATE_TRUNC('month', ufw.first_watch_date)
)
SELECT 
    cohort_month,
    cohort_size,
    retained_users,
    ROUND((retained_users::DECIMAL / cohort_size) * 100, 2) as retention_rate_30d
FROM cohort_analysis
ORDER BY cohort_month;

-- 6. Content Genre Performance
WITH genre_analysis AS (
    SELECT 
        jsonb_array_elements_text(c.genre) as genre_name,
        COUNT(vs.session_id) as total_sessions,
        AVG(vs.completion_percentage) as avg_completion,
        AVG(vs.watch_duration_minutes) as avg_duration,
        COUNT(DISTINCT vs.user_id) as unique_viewers
    FROM content c
    LEFT JOIN viewing_sessions vs ON c.content_id = vs.content_id
    GROUP BY jsonb_array_elements_text(c.genre)
)
SELECT 
    genre_name,
    total_sessions,
    ROUND(avg_completion, 2) as avg_completion,
    ROUND(avg_duration, 2) as avg_duration,
    unique_viewers,
    ROUND((total_sessions::DECIMAL / unique_viewers), 2) as sessions_per_viewer
FROM genre_analysis
WHERE genre_name IS NOT NULL
ORDER BY total_sessions DESC;

-- 7. Peak Usage Analysis
SELECT 
    EXTRACT(HOUR FROM watch_date::timestamp) as hour_of_day,
    EXTRACT(DOW FROM watch_date) as day_of_week,
    COUNT(*) as session_count,
    AVG(completion_percentage) as avg_completion,
    AVG(watch_duration_minutes) as avg_duration
FROM viewing_sessions
GROUP BY EXTRACT(HOUR FROM watch_date::timestamp), EXTRACT(DOW FROM watch_date)
ORDER BY day_of_week, hour_of_day;
