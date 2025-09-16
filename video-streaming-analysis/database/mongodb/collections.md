# MongoDB Collections Design

## users
- _id: user_id (string)
- age: int
- country: string
- subscription_type: string
- registration_date: date
- total_watch_time_hours: number

## content
- _id: content_id (string)
- title: string
- genre: [string]
- duration_minutes: int
- release_year: int
- rating: number
- views_count: int
- production_budget: number
- content_type: string ('movie' for provided data)

## viewing_sessions
- _id: session_id (string)
- user_id: string (ref users)
- content_id: string (ref content)
- watch_date: date
- watch_duration_minutes: int
- completion_percentage: number
- device_type: string
- quality_level: string
