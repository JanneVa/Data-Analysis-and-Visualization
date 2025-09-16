#!/usr/bin/env python3
"""
Script para levantar contenedores Docker y ejecutar la inserción de datos
"""

import subprocess
import time
import sys
import os

def run_command(command, description):
    """Ejecutar comando y mostrar resultado"""
    print(f"🔄 {description}...")
    try:
        result = subprocess.run(command, shell=True, capture_output=True, text=True)
        if result.returncode == 0:
            print(f"✅ {description} - Completado")
            if result.stdout:
                print(result.stdout)
        else:
            print(f"❌ {description} - Error")
            print(result.stderr)
            return False
        return True
    except Exception as e:
        print(f"❌ Error ejecutando: {description} - {e}")
        return False

def check_docker():
    """Verificar que Docker esté instalado y ejecutándose"""
    print("🐳 Verificando Docker...")
    if not run_command("docker --version", "Verificar Docker"):
        print("❌ Docker no está instalado o no está ejecutándose")
        print("💡 Instala Docker Desktop y asegúrate de que esté ejecutándose")
        return False
    return True

def start_containers():
    """Levantar contenedores Docker"""
    print("\n🚀 LEVANTANDO CONTENEDORES DOCKER")
    print("=" * 50)
    
    # Detener contenedores existentes si los hay
    run_command("docker-compose down", "Detener contenedores existentes")
    
    # Levantar contenedores
    if not run_command("docker-compose up -d", "Levantar contenedores PostgreSQL y MongoDB"):
        return False
    
    # Esperar a que los contenedores estén listos
    print("⏳ Esperando a que los contenedores estén listos...")
    time.sleep(10)
    
    # Verificar que los contenedores estén ejecutándose
    if not run_command("docker ps", "Verificar estado de contenedores"):
        return False
    
    return True

def wait_for_databases():
    """Esperar a que las bases de datos estén listas"""
    print("\n⏳ Esperando a que las bases de datos estén listas...")
    
    # Esperar PostgreSQL
    print("🔄 Esperando PostgreSQL...")
    for i in range(30):  # Esperar hasta 30 segundos
        if run_command("docker exec video_streaming_postgres pg_isready -U postgres", "Verificar PostgreSQL"):
            print("✅ PostgreSQL está listo")
            break
        time.sleep(1)
    else:
        print("❌ PostgreSQL no está respondiendo")
        return False
    
    # Esperar MongoDB
    print("🔄 Esperando MongoDB...")
    for i in range(30):  # Esperar hasta 30 segundos
        if run_command("docker exec video_streaming_mongodb mongosh --eval 'db.runCommand(\"ping\")'", "Verificar MongoDB"):
            print("✅ MongoDB está listo")
            break
        time.sleep(1)
    else:
        print("❌ MongoDB no está respondiendo")
        return False
    
    return True

def install_dependencies():
    """Instalar dependencias de Python"""
    print("\n📦 INSTALANDO DEPENDENCIAS")
    print("=" * 30)
    
    dependencies = [
        'pandas',
        'psycopg2-binary',
        'pymongo',
        'numpy',
        'matplotlib',
        'seaborn',
        'plotly',
        'streamlit',
        'scikit-learn',
        'scipy'
    ]
    
    for dep in dependencies:
        if not run_command(f"pip install {dep}", f"Instalando {dep}"):
            print(f"⚠️  Error instalando {dep}, continuando...")

def run_data_insertion():
    """Ejecutar inserción de datos"""
    print("\n📊 INSERTANDO DATOS")
    print("=" * 30)
    
    # Verificar que los archivos de datos existan
    required_files = ['users.csv', 'viewing_sessions.csv', 'content.json']
    missing_files = [f for f in required_files if not os.path.exists(f)]
    
    if missing_files:
        print(f"❌ Archivos faltantes: {', '.join(missing_files)}")
        return False
    
    # Ejecutar inserción en PostgreSQL
    if not run_command("python3 insert_data.py", "Insertar datos en PostgreSQL"):
        return False
    
    # Ejecutar inserción en MongoDB
    if not run_command("python3 video-streaming-analysis/src/etl/load_to_mongo.py", "Insertar datos en MongoDB"):
        return False
    
    return True

def show_connection_info():
    """Mostrar información de conexión"""
    print("\n🔗 INFORMACIÓN DE CONEXIÓN")
    print("=" * 40)
    print("PostgreSQL:")
    print("  Host: localhost")
    print("  Puerto: 5432")
    print("  Base de datos: video_streaming_platform")
    print("  Usuario: postgres")
    print("  Contraseña: postgres")
    print()
    print("MongoDB:")
    print("  Host: localhost")
    print("  Puerto: 27017")
    print("  Base de datos: video_streaming_platform")
    print("  Usuario: admin")
    print("  Contraseña: admin123")
    print()
    print("Para conectar desde aplicaciones:")
    print("  PostgreSQL: postgresql://postgres:postgres@localhost:5432/video_streaming_platform")
    print("  MongoDB: mongodb://admin:admin123@localhost:27017/video_streaming_platform")

def main():
    """Función principal"""
    print("�� VIDEO STREAMING PLATFORM - DOCKER SETUP")
    print("=" * 60)
    
    # Verificar Docker
    if not check_docker():
        sys.exit(1)
    
    # Levantar contenedores
    if not start_containers():
        print("❌ Error levantando contenedores")
        sys.exit(1)
    
    # Esperar a que las bases de datos estén listas
    if not wait_for_databases():
        print("❌ Las bases de datos no están respondiendo")
        sys.exit(1)
    
    # Instalar dependencias
    install_dependencies()
    
    # Insertar datos
    if not run_data_insertion():
        print("❌ Error insertando datos")
        sys.exit(1)
    
    # Mostrar información de conexión
    show_connection_info()
    
    print("\n🎉 ¡SETUP COMPLETADO EXITOSAMENTE!")
    print("=" * 50)
    print("Los contenedores están ejecutándose. Para detenerlos:")
    print("  docker-compose down")
    print()
    print("Para ver los logs:")
    print("  docker-compose logs -f")
    print()
    print("Para ejecutar análisis:")
    print("  python3 proyect.py")

if __name__ == "__main__":
    main()
