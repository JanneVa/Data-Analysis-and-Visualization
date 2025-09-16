import os
import json
import pandas as pd
from sqlalchemy import create_engine, text
from sqlalchemy.types import Integer, String, Date, Float, JSON

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../..'))
USERS_CSV = os.path.join(BASE_DIR, 'users.csv')
SESSIONS_CSV = os.path.join(BASE_DIR, 'viewing_sessions.csv')
CONTENT_JSON = os.path.join(BASE_DIR, 'content.json')
SCHEMA_SQL = os.path.join(BASE_DIR, 'video-streaming-analysis/database/sql/schema.sql')

PG_HOST = os.getenv('PG_HOST', 'localhost')
PG_PORT = int(os.getenv('PG_PORT', '5432'))
PG_DB = os.getenv('PG_DB', 'video_streaming_platform')
PG_USER = os.getenv('PG_USER', 'postgres')
PG_PASSWORD = os.getenv('PG_PASSWORD', 'postgres')

engine = create_engine(f'postgresql+psycopg2://{PG_USER}:{PG_PASSWORD}@{PG_HOST}:{PG_PORT}/{PG_DB}')


def ensure_schema():
    with engine.begin() as conn:
        with open(SCHEMA_SQL, 'r', encoding='utf-8') as f:
            conn.execute(text(f.read()))


def load_users():
    df = pd.read_csv(USERS_CSV)
    df.to_sql(
        'users', engine, if_exists='append', index=False,
        dtype={
            'user_id': String(20),
            'age': Integer(),
            'country': String(100),
            'subscription_type': String(50),
            'registration_date': Date(),
            'total_watch_time_hours': Float(),
        }
    )


def load_content():
    with open(CONTENT_JSON, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    records = []
    
    # Process movies
    movies = data.get('movies', [])
    for m in movies:
        records.append({
            'content_id': m.get('content_id'),
            'title': m.get('title'),
            'genre': m.get('genre'),
            'content_type': 'movie',
            'duration_minutes': m.get('duration_minutes'),
            'release_year': m.get('release_year'),
            'rating': m.get('rating'),
            'views_count': m.get('views_count'),
            'production_budget': m.get('production_budget'),
            'seasons': None,
            'episodes_per_season': None,
            'avg_episode_duration': None,
        })
    
    # Process series
    series = data.get('series', [])
    for s in series:
        records.append({
            'content_id': s.get('content_id'),
            'title': s.get('title'),
            'genre': s.get('genre'),
            'content_type': 'series',
            'duration_minutes': s.get('avg_episode_duration'),  # Use avg_episode_duration
            'release_year': None,  # Not provided in series data
            'rating': s.get('rating'),
            'views_count': s.get('total_views'),
            'production_budget': s.get('production_budget'),
            'seasons': s.get('seasons'),
            'episodes_per_season': s.get('episodes_per_season'),
            'avg_episode_duration': s.get('avg_episode_duration'),
        })
    
    df = pd.DataFrame.from_records(records)
    df.to_sql(
        'content', engine, if_exists='append', index=False,
        dtype={
            'content_id': String(20),
            'title': String(255),
            'genre': JSON(),
            'content_type': String(20),
            'duration_minutes': Integer(),
            'release_year': Integer(),
            'rating': Float(),
            'views_count': Integer(),
            'production_budget': Integer(),
            'seasons': Integer(),
            'episodes_per_season': JSON(),
            'avg_episode_duration': Integer(),
        }
    )


def load_viewing_sessions():
    df = pd.read_csv(SESSIONS_CSV)
    df.to_sql(
        'viewing_sessions', engine, if_exists='append', index=False,
        dtype={
            'session_id': String(20),
            'user_id': String(20),
            'content_id': String(20),
            'watch_date': Date(),
            'watch_duration_minutes': Integer(),
            'completion_percentage': Float(),
            'device_type': String(50),
            'quality_level': String(20),
        }
    )


def main():
    ensure_schema()
    load_users()
    load_content()
    load_viewing_sessions()
    print('ETL to PostgreSQL completed successfully.')


if __name__ == '__main__':
    main()
