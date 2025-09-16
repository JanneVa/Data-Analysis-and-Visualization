#!/usr/bin/env python3
"""
Script para configurar la base de datos PostgreSQL
Crea la base de datos y configura el usuario si es necesario
"""

import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
import sys

def create_database():
    """Crear la base de datos si no existe"""
    try:
        # Conectar a la base de datos por defecto (postgres)
        conn = psycopg2.connect(
            host='localhost',
            port=5432,
            database='postgres',
            user='postgres',
            password='postgres'
        )
        conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
        cursor = conn.cursor()
        
        # Verificar si la base de datos existe
        cursor.execute("SELECT 1 FROM pg_database WHERE datname = 'video_streaming_platform'")
        exists = cursor.fetchone()
        
        if not exists:
            # Crear la base de datos
            cursor.execute('CREATE DATABASE video_streaming_platform')
            print("✅ Base de datos 'video_streaming_platform' creada")
        else:
            print("ℹ️  Base de datos 'video_streaming_platform' ya existe")
        
        cursor.close()
        conn.close()
        
    except psycopg2.Error as e:
        print(f"❌ Error creando base de datos: {e}")
        print("\n💡 Asegúrate de que:")
        print("   - PostgreSQL esté instalado y ejecutándose")
        print("   - El usuario 'postgres' tenga permisos")
        print("   - La contraseña sea 'postgres' (o modifica el script)")
        sys.exit(1)

def test_connection():
    """Probar la conexión a la base de datos"""
    try:
        conn = psycopg2.connect(
            host='localhost',
            port=5432,
            database='video_streaming_platform',
            user='postgres',
            password='postgres'
        )
        cursor = conn.cursor()
        cursor.execute('SELECT version();')
        version = cursor.fetchone()[0]
        print(f"✅ Conexión exitosa a PostgreSQL: {version}")
        cursor.close()
        conn.close()
        return True
    except psycopg2.Error as e:
        print(f"❌ Error conectando a la base de datos: {e}")
        return False

def main():
    """Función principal"""
    print("🔧 CONFIGURANDO BASE DE DATOS")
    print("=" * 40)
    
    # Crear base de datos
    create_database()
    
    # Probar conexión
    if test_connection():
        print("\n🎉 Base de datos configurada correctamente!")
        print("Ahora puedes ejecutar: python insert_data.py")
    else:
        print("\n❌ Error en la configuración de la base de datos")
        sys.exit(1)

if __name__ == "__main__":
    main()
