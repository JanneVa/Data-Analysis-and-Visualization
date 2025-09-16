#!/usr/bin/env python3
"""
Script para instalar dependencias necesarias
"""

import subprocess
import sys
import os

def install_package(package):
    """Instalar un paquete usando pip"""
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", package])
        return True
    except subprocess.CalledProcessError:
        return False

def main():
    """Instalar todas las dependencias necesarias"""
    print("📦 INSTALANDO DEPENDENCIAS")
    print("=" * 40)
    
    # Lista de paquetes necesarios
    packages = [
        'pandas',
        'psycopg2-binary',
        'numpy',
        'matplotlib',
        'seaborn',
        'plotly',
        'streamlit',
        'scikit-learn',
        'scipy',
        'jupyter'
    ]
    
    failed_packages = []
    
    for package in packages:
        print(f"Instalando {package}...", end=" ")
        if install_package(package):
            print("✅")
        else:
            print("❌")
            failed_packages.append(package)
    
    if failed_packages:
        print(f"\n⚠️  Paquetes que fallaron: {', '.join(failed_packages)}")
        print("Intenta instalarlos manualmente con: pip install <paquete>")
    else:
        print("\n🎉 Todas las dependencias instaladas correctamente!")
    
    # Verificar PostgreSQL
    print("\n🔍 Verificando PostgreSQL...")
    try:
        import psycopg2
        print("✅ psycopg2 instalado correctamente")
    except ImportError:
        print("❌ psycopg2 no se pudo importar")
        print("💡 Asegúrate de tener PostgreSQL instalado en tu sistema")

if __name__ == "__main__":
    main()
