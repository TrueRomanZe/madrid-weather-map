"""
Script de actualización de datos meteorológicos para municipios de la Comunidad de Madrid.
Este script se ejecuta automáticamente cada 3 horas mediante GitHub Actions.

El script realiza las siguientes operaciones:
1. Lee el archivo GeoJSON con los límites municipales
2. Calcula el centroide de cada municipio
3. Consulta la API de OpenWeatherMap para obtener datos meteorológicos
4. Evalúa las condiciones climáticas según criterios predefinidos
5. Genera un archivo JSON con toda la información procesada

Autor: [Tu Nombre]
Licencia: MIT
Fuentes de datos:
- Datos meteorológicos: OpenWeatherMap (https://openweathermap.org)
- Datos geográficos: ESRI/IGN España
"""

import json
import requests
from datetime import datetime
import time
import os
import sys


# ============================================================================
# CONFIGURACIÓN GLOBAL
# ============================================================================

# La API key se obtiene de las variables de entorno por seguridad
OPENWEATHER_API_KEY = os.environ.get('OPENWEATHER_API_KEY')

# Rutas de archivos
GEOJSON_FILE = 'data/municipios_madrid.geojson'
OUTPUT_FILE = 'data/weather_data.json'

# Criterios para evaluar las condiciones meteorológicas
# Estos valores pueden ajustarse según las preferencias del usuario
CRITERIOS = {
    'temp_optima_min': 15,      # Temperatura mínima ideal en °C
    'temp_optima_max': 25,      # Temperatura máxima ideal en °C
    'temp_precaucion_min': 8,   # Por debajo requiere abrigo
    'temp_precaucion_max': 32,  # Por encima requiere precaución por calor
    'viento_precaucion': 20,    # Velocidad del viento en km/h que requiere precaución
    'viento_peligroso': 40,     # Velocidad del viento considerada peligrosa en km/h
    'lluvia_ligera': 2,         # Precipitación en mm/h considerada ligera
    'lluvia_fuerte': 7.6        # Precipitación en mm/h considerada fuerte
}


# ============================================================================
# FUNCIONES DE PROCESAMIENTO GEOMÉTRICO
# ============================================================================

def calcular_centroide(geometry):
    """
    Calcula el centroide (centro geométrico) de una geometría GeoJSON.
    
    Esta función maneja tanto polígonos simples (Polygon) como polígonos
    múltiples (MultiPolygon). El centroide se calcula como el promedio
    aritmético de todas las coordenadas que componen el polígono.
    
    Args:
        geometry: Diccionario con la geometría en formato GeoJSON
        
    Returns:
        Tupla (longitud, latitud) del centroide
        
    Raises:
        ValueError: Si el tipo de geometría no es soportado
    """
    geom_type = geometry['type']
    coords = geometry['coordinates']
    
    # Para polígonos simples, tomamos el anillo exterior (primer elemento)
    if geom_type == 'Polygon':
        ring = coords[0]
    # Para multipolígonos, tomamos el anillo exterior del primer polígono
    elif geom_type == 'MultiPolygon':
        ring = coords[0][0]
    else:
        raise ValueError(f"Tipo de geometría no soportado: {geom_type}")
    
    # Calcular el promedio de todas las coordenadas
    # Nota: en GeoJSON las coordenadas están en formato [longitud, latitud]
    longitudes = [coord[0] for coord in ring]
    latitudes = [coord[1] for coord in ring]
    
    lon_centro = sum(longitudes) / len(longitudes)
    lat_centro = sum(latitudes) / len(latitudes)
    
    return lon_centro, lat_centro


# ============================================================================
# FUNCIONES DE CONSULTA A LA API
# ============================================================================

def obtener_datos_clima(lat, lon, nombre_municipio):
    """
    Consulta la API de OpenWeatherMap para obtener datos meteorológicos
    de un punto geográfico específico.
    
    La función realiza una petición HTTP a la API de OpenWeatherMap usando
    las coordenadas proporcionadas. Los datos se obtienen en unidades métricas
    (temperatura en Celsius, velocidad del viento en m/s) y en español.
    
    Args:
        lat: Latitud del punto a consultar (float)
        lon: Longitud del punto a consultar (float)
        nombre_municipio: Nombre del municipio (string, solo para logging)
        
    Returns:
        Diccionario con los datos meteorológicos en formato de OpenWeatherMap,
        o None si ocurre algún error en la petición.
        
    Nota:
        La función incluye un timeout de 10 segundos para evitar bloqueos
        indefinidos en caso de problemas de red.
    """
    url = "https://api.openweathermap.org/data/2.5/weather"
    
    params = {
        'lat': lat,
        'lon': lon,
        'appid': OPENWEATHER_API_KEY,
        'units': 'metric',  # Obtener temperatura en Celsius y viento en m/s
        'lang': 'es'        # Descripciones del clima en español
    }
    
    try:
        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()  # Lanza excepción si el código de respuesta indica error
        return response.json()
    
    except requests.exceptions.Timeout:
        print(f"⚠️  Timeout al consultar {nombre_municipio} - la API tardó más de 10 segundos")
        return None
    
    except requests.exceptions.HTTPError as e:
        print(f"⚠️  Error HTTP al consultar {nombre_municipio}: {e}")
        return None
    
    except requests.exceptions.RequestException as e:
        print(f"⚠️  Error de red al consultar {nombre_municipio}: {e}")
        return None


# ============================================================================
# FUNCIONES DE EVALUACIÓN DEL CLIMA
# ============================================================================

def calcular_indice_tiempo(datos_clima):
    """
    Calcula un índice de calidad del tiempo basado en múltiples variables
    meteorológicas y genera recomendaciones para el usuario.
    
    El sistema funciona con una puntuación de 0 a 100 puntos, donde 100
    representa condiciones perfectas para actividades al aire libre. Se
    evalúan múltiples factores: temperatura, sensación térmica, viento,
    precipitación y nieve. Cada factor adverso reduce la puntuación.
    
    Clasificación final:
    - Verde (70-100 puntos): Condiciones óptimas
    - Amarillo (40-69 puntos): Condiciones aceptables con precauciones
    - Rojo (0-39 puntos): Condiciones adversas
    
    Args:
        datos_clima: Diccionario con datos meteorológicos de OpenWeatherMap
        
    Returns:
        Diccionario con las siguientes claves:
        - nivel: 'verde', 'amarillo', 'rojo' o 'sin-datos'
        - puntuacion: Valor numérico de 0 a 100
        - mensaje: Texto breve describiendo la condición general
        - consejos: Lista de strings con recomendaciones específicas
        - color: Código hexadecimal del color para visualización
    """
    
    # Manejo del caso sin datos disponibles
    if not datos_clima:
        return {
            'nivel': 'sin-datos',
            'puntuacion': 0,
            'mensaje': 'Datos no disponibles',
            'consejos': ['No hay datos meteorológicos disponibles para este municipio'],
            'color': '#9ca3af'
        }
    
    # ========================================================================
    # EXTRACCIÓN DE VARIABLES METEOROLÓGICAS
    # ========================================================================
    
    # Variables principales (siempre presentes)
    temp = datos_clima['main']['temp']
    sensacion = datos_clima['main']['feels_like']
    humedad = datos_clima['main']['humidity']
    viento_ms = datos_clima['wind']['speed']
    viento = viento_ms * 3.6  # Convertir de m/s a km/h para facilitar interpretación
    
    # Variables opcionales (solo presentes si hay precipitación)
    lluvia = 0
    if 'rain' in datos_clima and '1h' in datos_clima['rain']:
        lluvia = datos_clima['rain']['1h']
    
    nieve = 0
    if 'snow' in datos_clima and '1h' in datos_clima['snow']:
        nieve = datos_clima['snow']['1h']
    
    # ========================================================================
    # SISTEMA DE PUNTUACIÓN Y GENERACIÓN DE CONSEJOS
    # ========================================================================
    
    puntuacion = 100  # Comenzamos con puntuación perfecta
    consejos = []     # Lista de recomendaciones para el usuario
    
    # Evaluación de temperatura
    # El rango óptimo de temperatura es el más cómodo para actividades al aire libre
    if CRITERIOS['temp_optima_min'] <= temp <= CRITERIOS['temp_optima_max']:
        # Temperatura perfecta, no hay penalización
        pass
    elif CRITERIOS['temp_precaucion_min'] <= temp < CRITERIOS['temp_optima_min']:
        # Temperatura fresca pero tolerable
        puntuacion -= 20
        consejos.append('🧥 Hace algo de frío, lleva una chaqueta o abrigo ligero')
    elif CRITERIOS['temp_optima_max'] < temp <= CRITERIOS['temp_precaucion_max']:
        # Temperatura cálida pero manejable
        puntuacion -= 20
        consejos.append('☀️ Hace calor, lleva agua y protección solar (gorra, crema)')
    elif temp < CRITERIOS['temp_precaucion_min']:
        # Temperatura fría que requiere precauciones importantes
        puntuacion -= 50
        consejos.append('❄️ Hace mucho frío, abrígate bien con varias capas de ropa')
    else:  # temp > temp_precaucion_max
        # Temperatura muy alta que puede ser peligrosa
        puntuacion -= 50
        consejos.append('🌡️ Hace mucho calor, evita exposición prolongada al sol')
    
    # Evaluación de sensación térmica
    # Si la sensación térmica difiere significativamente de la temperatura real,
    # el usuario debe saberlo porque afecta cómo se sentirá al estar fuera
    diferencia_termica = abs(sensacion - temp)
    if diferencia_termica > 5:
        puntuacion -= 10
        if sensacion < temp:
            consejos.append('🌬️ El viento hace que se sienta más frío de lo que indica la temperatura')
        else:
            consejos.append('💧 La humedad hace que se sienta más calor del real')
    
    # Evaluación del viento
    # El viento puede hacer incómodas o peligrosas las actividades al aire libre
    if viento < CRITERIOS['viento_precaucion']:
        # Viento suave o brisa, ideal
        pass
    elif viento < CRITERIOS['viento_peligroso']:
        # Viento moderado que requiere tomar precauciones
        puntuacion -= 25
        consejos.append(f'💨 Viento moderado ({int(viento)} km/h), sujeta bien tus pertenencias')
    else:
        # Viento fuerte que puede ser peligroso
        puntuacion -= 60
        consejos.append(f'⚠️ Viento fuerte ({int(viento)} km/h), peligroso para actividades al aire libre')
    
    # Evaluación de precipitación (lluvia)
    # Cualquier cantidad de lluvia afecta negativamente las actividades al aire libre
    if lluvia == 0:
        # Sin lluvia, perfecto
        pass
    elif lluvia < CRITERIOS['lluvia_ligera']:
        # Llovizna o lluvia muy ligera
        puntuacion -= 20
        consejos.append('🌦️ Lluvia ligera, lleva paraguas o impermeable')
    elif lluvia < CRITERIOS['lluvia_fuerte']:
        # Lluvia moderada que dificulta las actividades
        puntuacion -= 40
        consejos.append('☔ Lluvia moderada, mejor postponer actividades al aire libre')
    else:
        # Lluvia fuerte, muy desaconsejable salir
        puntuacion -= 70
        consejos.append('⛈️ Lluvia fuerte, no es buen momento para salir')
    
    # Evaluación de nieve
    # La presencia de nieve siempre requiere precauciones especiales
    if nieve > 0:
        puntuacion -= 50
        consejos.append('🌨️ Está nevando, extrema precaución con superficies resbaladizas')
    
    # ========================================================================
    # CLASIFICACIÓN FINAL Y GENERACIÓN DE MENSAJE
    # ========================================================================
    
    # Asegurar que la puntuación no sea negativa
    puntuacion = max(0, puntuacion)
    
    # Si no hay consejos específicos, las condiciones son perfectas
    if not consejos:
        consejos.append('✨ Condiciones perfectas para actividades al aire libre')
    
    # Determinar el nivel de recomendación según la puntuación final
    if puntuacion >= 70:
        nivel = 'verde'
        color = '#10b981'  # Verde brillante
        mensaje_general = 'Excelente para salir'
    elif puntuacion >= 40:
        nivel = 'amarillo'
        color = '#f59e0b'  # Naranja/Amarillo
        mensaje_general = 'Aceptable con precauciones'
    else:
        nivel = 'rojo'
        color = '#ef4444'  # Rojo
        mensaje_general = 'Mejor quedarse en casa'
    
    return {
        'nivel': nivel,
        'puntuacion': puntuacion,
        'mensaje': mensaje_general,
        'consejos': consejos,
        'color': color
    }


# ============================================================================
# FUNCIÓN PRINCIPAL DE PROCESAMIENTO
# ============================================================================

def procesar_municipios():
    """
    Función principal que coordina todo el proceso de actualización.
    
    Esta función realiza las siguientes operaciones en secuencia:
    1. Valida la presencia de la API key
    2. Lee el archivo GeoJSON con los municipios
    3. Para cada municipio:
       - Calcula su centroide
       - Consulta los datos meteorológicos
       - Evalúa las condiciones y genera recomendaciones
    4. Guarda todos los datos procesados en un archivo JSON
    
    El proceso incluye manejo de errores robusto y logging detallado
    para facilitar la detección y resolución de problemas.
    """
    
    print("=" * 70)
    print("🚀 INICIANDO ACTUALIZACIÓN DE DATOS METEOROLÓGICOS")
    print("=" * 70)
    print(f"⏰ Hora de inicio: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()
    
    # ========================================================================
    # VALIDACIÓN DE REQUISITOS PREVIOS
    # ========================================================================
    
    # Verificar que existe la API key en las variables de entorno
    if not OPENWEATHER_API_KEY:
        print("❌ ERROR CRÍTICO: No se encontró OPENWEATHER_API_KEY")
        print("   La variable de entorno debe configurarse antes de ejecutar el script")
        sys.exit(1)
    
    print("✅ API key de OpenWeatherMap encontrada")
    
    # ========================================================================
    # LECTURA DEL ARCHIVO GEOJSON
    # ========================================================================
    
    print(f"📂 Leyendo archivo GeoJSON: {GEOJSON_FILE}")
    
    try:
        with open(GEOJSON_FILE, 'r', encoding='utf-8') as f:
            geojson = json.load(f)
    except FileNotFoundError:
        print(f"❌ ERROR: No se encontró el archivo {GEOJSON_FILE}")
        print("   Asegúrate de que el archivo existe en la ubicación correcta")
        sys.exit(1)
    except json.JSONDecodeError as e:
        print(f"❌ ERROR: El archivo GeoJSON no tiene formato válido")
        print(f"   Detalle del error: {e}")
        sys.exit(1)
    
    # Validar estructura básica del GeoJSON
    if 'features' not in geojson:
        print("❌ ERROR: El archivo GeoJSON no contiene la clave 'features'")
        sys.exit(1)
    
    total_municipios = len(geojson['features'])
    print(f"✅ Archivo GeoJSON cargado correctamente")
    print(f"📍 Total de municipios a procesar: {total_municipios}")
    print()
    
    # ========================================================================
    # PROCESAMIENTO DE CADA MUNICIPIO
    # ========================================================================
    
    municipios_procesados = []
    municipios_con_error = []
    
    print("🔄 Iniciando procesamiento de municipios...")
    print("-" * 70)
    
    for idx, feature in enumerate(geojson['features'], 1):
        # Extraer información del municipio
        properties = feature['properties']
        geometry = feature['geometry']
        
        # Obtener el nombre del municipio (campo NAMEUNIT del IGN/ESRI)
        nombre = properties.get('NAMEUNIT', 'Desconocido')
        codigo_ine = properties.get('NATCODE', '')
        
        print(f"[{idx}/{total_municipios}] Procesando: {nombre}")
        
        try:
            # Calcular el centroide del municipio
            lon_centro, lat_centro = calcular_centroide(geometry)
            
            # Consultar datos meteorológicos para este punto
            datos_clima = obtener_datos_clima(lat_centro, lon_centro, nombre)
            
            if datos_clima:
                # Calcular el índice de buen tiempo
                indice = calcular_indice_tiempo(datos_clima)
                
                # Preparar datos estructurados en formato GeoJSON válido
                # Cada municipio debe ser un Feature GeoJSON completo
                municipio_data = {
                    'type': 'Feature',
                    'properties': {
                        'nombre': nombre,
                        'codigo_ine': codigo_ine,
                        'coordenadas': {
                            'lat': round(lat_centro, 6),
                            'lon': round(lon_centro, 6)
                        },
                        'clima': {
                            'temperatura': round(datos_clima['main']['temp'], 1),
                            'sensacion': round(datos_clima['main']['feels_like'], 1),
                            'humedad': datos_clima['main']['humidity'],
                            'viento': round(datos_clima['wind']['speed'] * 3.6, 1),
                            'descripcion': datos_clima['weather'][0]['description'],
                            'icono': datos_clima['weather'][0]['icon']
                        },
                        'indice': indice
                    },
                    'geometry': geometry  # Geometría original del municipio
                }
                
                municipios_procesados.append(municipio_data)
                print(f"    ✓ Completado - Nivel: {indice['nivel']} ({indice['puntuacion']} pts)")
            else:
                municipios_con_error.append(nombre)
                print(f"    ✗ Error al obtener datos meteorológicos")
        
        except Exception as e:
            municipios_con_error.append(nombre)
            print(f"    ✗ Error inesperado: {e}")
        
        # Pausa entre llamadas a la API para respetar los límites de tasa
        # OpenWeatherMap permite 60 llamadas por minuto en el plan gratuito
        time.sleep(1)
    
    # ========================================================================
    # GENERACIÓN DEL ARCHIVO DE SALIDA
    # ========================================================================
    
    print()
    print("-" * 70)
    print("💾 Guardando datos procesados...")
    
    # Crear estructura del archivo JSON de salida con metadata
    datos_finales = {
        'metadata': {
            'ultima_actualizacion': datetime.now().isoformat(),
            'ultima_actualizacion_formateada': datetime.now().strftime('%d/%m/%Y a las %H:%M'),
            'total_municipios': len(municipios_procesados),
            'municipios_con_error': len(municipios_con_error),
            'fuente_clima': 'OpenWeatherMap',
            'fuente_geodatos': 'ESRI/IGN España',
            'version_script': '2.0'
        },
        'municipios': municipios_procesados
    }
    
    # Guardar en archivo JSON con formato legible
    try:
        with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
            json.dump(datos_finales, f, ensure_ascii=False, indent=2)
        print(f"✅ Datos guardados correctamente en: {OUTPUT_FILE}")
    except Exception as e:
        print(f"❌ ERROR al guardar el archivo: {e}")
        sys.exit(1)
    
    # ========================================================================
    # RESUMEN FINAL
    # ========================================================================
    
    print()
    print("=" * 70)
    print("✅ PROCESO COMPLETADO EXITOSAMENTE")
    print("=" * 70)
    print(f"📊 Municipios procesados correctamente: {len(municipios_procesados)}")
    if municipios_con_error:
        print(f"⚠️  Municipios con errores: {len(municipios_con_error)}")
        print(f"   Municipios afectados: {', '.join(municipios_con_error[:5])}")
        if len(municipios_con_error) > 5:
            print(f"   ... y {len(municipios_con_error) - 5} más")
    print(f"⏰ Hora de finalización: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 70)


# ============================================================================
# PUNTO DE ENTRADA DEL SCRIPT
# ============================================================================

if __name__ == "__main__":
    procesar_municipios()
