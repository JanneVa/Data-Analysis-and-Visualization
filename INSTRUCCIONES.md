# Instrucciones para Video Streaming Platform Analysis

## 📋 Requisitos Previos

### 1. PostgreSQL
- Instalar PostgreSQL en tu sistema
- Asegúrate de que el servicio esté ejecutándose
- Usuario por defecto: `postgres`
- Contraseña por defecto: `postgres`

### 2. Python 3.8+
- Verificar versión: `python3 --version`

## 🚀 Instalación y Configuración

### Paso 1: Instalar Dependencias
```bash
python3 install_dependencies.py
```

### Paso 2: Configurar Base de Datos
```bash
python3 setup_database.py
```

### Paso 3: Insertar Datos
```bash
python3 insert_data.py
```

## 📁 Archivos Necesarios

Asegúrate de tener estos archivos en el directorio actual:
- `users.csv` - Datos de usuarios
- `viewing_sessions.csv` - Sesiones de visualización
- `content.json` - Contenido (películas y series)

## 🔧 Configuración de Base de Datos

Si necesitas cambiar la configuración de la base de datos, edita estas variables en los scripts:

```python
DB_CONFIG = {
    'host': 'localhost',        # Cambiar si PostgreSQL está en otro servidor
    'port': 5432,              # Puerto de PostgreSQL
    'database': 'video_streaming_platform',
    'user': 'postgres',        # Tu usuario de PostgreSQL
    'password': 'postgres'     # Tu contraseña de PostgreSQL
}
```

## 📊 Verificación

Después de ejecutar `insert_data.py`, deberías ver:
- ✅ Usuarios insertados
- ✅ Contenido insertado (películas y series)
- ✅ Sesiones de visualización insertadas
- ✅ Verificación de integridad referencial

## 🎯 Próximos Pasos

Una vez que los datos estén en la base de datos:

1. **Ejecutar análisis completo:**
   ```bash
   python3 proyect.py
   ```

2. **Lanzar dashboard interactivo:**
   ```bash
   streamlit run video-streaming-analysis/src/visualization/app.py
   ```

3. **Generar ER diagrama:**
   ```bash
   python3 video-streaming-analysis/database/er_diagram.py
   ```

## 🐛 Solución de Problemas

### Error de conexión a PostgreSQL
- Verifica que PostgreSQL esté ejecutándose
- Comprueba usuario y contraseña
- Asegúrate de que el puerto 5432 esté disponible

### Error de permisos
- Ejecuta con permisos de administrador si es necesario
- Verifica que el usuario tenga permisos para crear bases de datos

### Archivos no encontrados
- Verifica que `users.csv`, `viewing_sessions.csv` y `content.json` estén en el directorio actual
- Comprueba que los archivos no estén corruptos

## 📈 Estructura de la Base de Datos

### Tablas Creadas:
- `users` - Información de usuarios
- `content` - Películas y series
- `viewing_sessions` - Sesiones de visualización

### Vistas Disponibles:
- `user_engagement_summary` - Resumen de engagement por usuario
- `content_performance_summary` - Rendimiento del contenido
- `content_type_analysis` - Análisis por tipo de contenido

## �� ¡Listo!

Una vez completados todos los pasos, tendrás:
- Base de datos configurada con todos los datos
- Scripts de análisis listos para ejecutar
- Dashboard interactivo funcionando
- Documentación completa del proyecto
