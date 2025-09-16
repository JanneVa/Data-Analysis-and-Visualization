#!/usr/bin/env python3
"""
Script para detener y limpiar contenedores Docker
"""

import subprocess
import sys

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
        return result.returncode == 0
    except Exception as e:
        print(f"❌ Error ejecutando: {description} - {e}")
        return False

def main():
    """Función principal"""
    print("🛑 DETENIENDO CONTENEDORES DOCKER")
    print("=" * 40)
    
    # Detener contenedores
    run_command("docker-compose down", "Detener contenedores")
    
    # Limpiar volúmenes (opcional)
    response = input("¿Deseas eliminar los volúmenes de datos? (y/N): ")
    if response.lower() in ['y', 'yes', 'sí', 'si']:
        run_command("docker-compose down -v", "Eliminar volúmenes de datos")
        print("⚠️  Todos los datos han sido eliminados")
    
    # Limpiar imágenes (opcional)
    response = input("¿Deseas eliminar las imágenes Docker? (y/N): ")
    if response.lower() in ['y', 'yes', 'sí', 'si']:
        run_command("docker rmi postgres:15 mongo:7", "Eliminar imágenes Docker")
    
    print("\n✅ Limpieza completada")

if __name__ == "__main__":
    main()
