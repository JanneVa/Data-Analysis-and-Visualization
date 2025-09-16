#!/usr/bin/env python3
"""
Script para insertar datos de JSON y CSV en la base de datos PostgreSQL
Video Streaming Platform
"""

import os
import json
import pandas as pd
import psycopg2
from psycopg2.extras import execute_values
import sys

# Configuración de la base de datos
DB_CONFIG = {
    'host': 'localhost',
    'port': 5432,
    'database': 'video_streaming_platform',
    'user': 'postgres',
    'password': 'postgres'
}

def connect_db():
    """Conectar a la base de datos PostgreSQL"""
    try:
        conn = psycopg2.connect(**DB_CONFIG)
        print("✅ Conectado a la base de datos PostgreSQL")
        return conn
    except psycopg2.Error as e:
        print(f"❌ Error conectando a la base de datos: {e}")
        sys.exit(1)

def create_schema(conn):
    """Crear el esquema de la base de datos"""
    try:
        cursor = conn.cursor()
        
        # Leer y ejecutar el schema
        schema_file = 'video-streaming-analysis/database/sql/schema.sql'
        if os.path.exists(schema_file):
            with open(schema_file, 'r', encoding='utf-8') as f:
                schema_sql = f.read()
            cursor.execute(schema_sql)
            conn.commit()
            print("✅ Esquema de base de datos creado/actualizado")
        else:
            print("⚠️  Archivo schema.sql no encontrado, continuando...")
        
        cursor.close()
    except psycopg2.Error as e:
        print(f"❌ Error creando esquema: {e}")
        conn.rollback()

def insert_users(conn, csv_file):
    """Insertar usuarios desde CSV"""
    try:
        print(f"📊 Cargando usuarios desde {csv_file}...")
        df = pd.read_csv(csv_file)
        
        cursor = conn.cursor()
        
        # Limpiar tabla existente
        cursor.execute("TRUNCATE TABLE users CASCADE;")
        
        # Preparar datos para inserción
        users_data = []
        for _, row in df.iterrows():
            users_data.append((
                row['user_id'],
                int(row['age']),
                row['country'],
                row['subscription_type'],
                row['registration_date'],
                float(row['total_watch_time_hours'])
            ))
        
        # Insertar datos
        insert_query = """
        INSERT INTO users (user_id, age, country, subscription_type, registration_date, total_watch_time_hours)
        VALUES %s
        """
        
        execute_values(cursor, insert_query, users_data)
        conn.commit()
        cursor.close()
        
        print(f"✅ {len(users_data)} usuarios insertados correctamente")
        
    except Exception as e:
        print(f"❌ Error insertando usuarios: {e}")
        conn.rollback()

def insert_content(conn, json_file):
    """Insertar contenido desde JSON"""
    try:
        print(f"🎬 Cargando contenido desde {json_file}...")
        
        with open(json_file, 'r', encoding='utf-8') as f:
            content_data = json.load(f)
        
        cursor = conn.cursor()
        
        # Limpiar tabla existente
        cursor.execute("TRUNCATE TABLE content CASCADE;")
        
        content_data_list = []
        
        # Procesar películas
        movies = content_data.get('movies', [])
        for movie in movies:
            content_data_list.append((
                movie['content_id'],
                movie['title'],
                json.dumps(movie['genre']),  # Convertir lista a JSON string
                'movie',
                movie['duration_minutes'],
                movie['release_year'],
                movie['rating'],
                movie['views_count'],
                movie['production_budget'],
                None,  # seasons
                None,  # episodes_per_season
                None   # avg_episode_duration
            ))
        
        # Procesar series
        series = content_data.get('series', [])
        for serie in series:
            content_data_list.append((
                serie['content_id'],
                serie['title'],
                json.dumps(serie['genre']),  # Convertir lista a JSON string
                'series',
                serie['avg_episode_duration'],
                None,  # release_year (no disponible para series)
                serie['rating'],
                serie['total_views'],
                serie['production_budget'],
                serie['seasons'],
                json.dumps(serie['episodes_per_season']),  # Convertir lista a JSON string
                serie['avg_episode_duration']
            ))
        
        # Insertar datos
        insert_query = """
        INSERT INTO content (content_id, title, genre, content_type, duration_minutes, 
                           release_year, rating, views_count, production_budget, 
                           seasons, episodes_per_season, avg_episode_duration)
        VALUES %s
        """
        
        execute_values(cursor, insert_query, content_data_list)
        conn.commit()
        cursor.close()
        
        print(f"✅ {len(content_data_list)} elementos de contenido insertados correctamente")
        print(f"   - Películas: {len(movies)}")
        print(f"   - Series: {len(series)}")
        
    except Exception as e:
        print(f"❌ Error insertando contenido: {e}")
        conn.rollback()

def insert_sessions(conn, csv_file):
    """Insertar sesiones de visualización desde CSV"""
    try:
        print(f"📺 Cargando sesiones desde {csv_file}...")
        df = pd.read_csv(csv_file)
        
        cursor = conn.cursor()
        
        # Limpiar tabla existente
        cursor.execute("TRUNCATE TABLE viewing_sessions CASCADE;")
        
        # Preparar datos para inserción
        sessions_data = []
        for _, row in df.iterrows():
            sessions_data.append((
                row['session_id'],
                row['user_id'],
                row['content_id'],
                row['watch_date'],
                int(row['watch_duration_minutes']),
                float(row['completion_percentage']),
                row['device_type'],
                row['quality_level']
            ))
        
        # Insertar datos en lotes para mejor rendimiento
        batch_size = 1000
        total_inserted = 0
        
        for i in range(0, len(sessions_data), batch_size):
            batch = sessions_data[i:i + batch_size]
            
            insert_query = """
            INSERT INTO viewing_sessions (session_id, user_id, content_id, watch_date, 
                                        watch_duration_minutes, completion_percentage, 
                                        device_type, quality_level)
            VALUES %s
            """
            
            execute_values(cursor, insert_query, batch)
            total_inserted += len(batch)
            
            if i % 5000 == 0:  # Mostrar progreso cada 5000 registros
                print(f"   Procesados {total_inserted}/{len(sessions_data)} sesiones...")
        
        conn.commit()
        cursor.close()
        
        print(f"✅ {total_inserted} sesiones de visualización insertadas correctamente")
        
    except Exception as e:
        print(f"❌ Error insertando sesiones: {e}")
        conn.rollback()

def verify_data(conn):
    """Verificar que los datos se insertaron correctamente"""
    try:
        cursor = conn.cursor()
        
        print("\n🔍 VERIFICACIÓN DE DATOS:")
        print("-" * 40)
        
        # Contar usuarios
        cursor.execute("SELECT COUNT(*) FROM users;")
        user_count = cursor.fetchone()[0]
        print(f"👥 Usuarios: {user_count:,}")
        
        # Contar contenido por tipo
        cursor.execute("SELECT content_type, COUNT(*) FROM content GROUP BY content_type;")
        content_counts = cursor.fetchall()
        total_content = 0
        for content_type, count in content_counts:
            print(f"🎬 {content_type.capitalize()}: {count:,}")
            total_content += count
        print(f"📊 Total contenido: {total_content:,}")
        
        # Contar sesiones
        cursor.execute("SELECT COUNT(*) FROM viewing_sessions;")
        session_count = cursor.fetchone()[0]
        print(f"📺 Sesiones: {session_count:,}")
        
        # Verificar integridad referencial
        cursor.execute("""
            SELECT COUNT(*) FROM viewing_sessions vs 
            LEFT JOIN users u ON vs.user_id = u.user_id 
            WHERE u.user_id IS NULL;
        """)
        orphan_sessions = cursor.fetchone()[0]
        
        cursor.execute("""
            SELECT COUNT(*) FROM viewing_sessions vs 
            LEFT JOIN content c ON vs.content_id = c.content_id 
            WHERE c.content_id IS NULL;
        """)
        orphan_content = cursor.fetchone()[0]
        
        if orphan_sessions == 0 and orphan_content == 0:
            print("✅ Integridad referencial: OK")
        else:
            print(f"⚠️  Sesiones huérfanas: {orphan_sessions}")
            print(f"⚠️  Contenido huérfano: {orphan_content}")
        
        cursor.close()
        
    except Exception as e:
        print(f"❌ Error verificando datos: {e}")

def main():
    """Función principal"""
    print("🚀 INICIANDO INSERCIÓN DE DATOS")
    print("=" * 50)
    
    # Verificar que los archivos existen
    required_files = ['users.csv', 'viewing_sessions.csv', 'content.json']
    missing_files = [f for f in required_files if not os.path.exists(f)]
    
    if missing_files:
        print(f"❌ Archivos faltantes: {', '.join(missing_files)}")
        print("Asegúrate de que los archivos estén en el directorio actual")
        sys.exit(1)
    
    # Conectar a la base de datos
    conn = connect_db()
    
    try:
        # Crear esquema
        create_schema(conn)
        
        # Insertar datos
        insert_users(conn, 'users.csv')
        insert_content(conn, 'content.json')
        insert_sessions(conn, 'viewing_sessions.csv')
        
        # Verificar datos
        verify_data(conn)
        
        print("\n🎉 INSERCIÓN COMPLETADA EXITOSAMENTE!")
        print("=" * 50)
        
    except Exception as e:
        print(f"❌ Error durante la inserción: {e}")
        conn.rollback()
    finally:
        conn.close()
        print("🔌 Conexión a base de datos cerrada")

if __name__ == "__main__":
    main()
