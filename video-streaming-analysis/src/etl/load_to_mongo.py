import os
import json
import pandas as pd
from pymongo import MongoClient

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../..'))
USERS_CSV = os.path.join(BASE_DIR, 'users.csv')
SESSIONS_CSV = os.path.join(BASE_DIR, 'viewing_sessions.csv')
CONTENT_JSON = os.path.join(BASE_DIR, 'content.json')

MONGO_URI = os.getenv('MONGO_URI', 'mongodb://localhost:27017')
DB_NAME = os.getenv('MONGO_DB', 'video_streaming_platform')

client = MongoClient(MONGO_URI)
db = client[DB_NAME]


def load_users():
    df = pd.read_csv(USERS_CSV)
    records = df.to_dict(orient='records')
    # Use user_id as _id for idempotency
    for r in records:
        r['_id'] = r['user_id']
    db.users.delete_many({})
    db.users.insert_many(records)


def load_content():
    with open(CONTENT_JSON, 'r', encoding='utf-8') as f:
        data = json.load(f)
    movies = data.get('movies', [])
    for m in movies:
        m['_id'] = m['content_id']
        m['content_type'] = 'movie'
    db.content.delete_many({})
    db.content.insert_many(movies)


def load_viewing_sessions():
    df = pd.read_csv(SESSIONS_CSV)
    records = df.to_dict(orient='records')
    for r in records:
        r['_id'] = r['session_id']
    db.viewing_sessions.delete_many({})
    db.viewing_sessions.insert_many(records)


def main():
    load_users()
    load_content()
    load_viewing_sessions()
    print('ETL to MongoDB completed successfully.')


if __name__ == '__main__':
    main()
