"""
Script para actualizar los datos meteorológicos de los municipios de la Comunidad de Madrid.
Este script se ejecuta automáticamente cada 3 horas mediante GitHub Actions.

Autor: Tu nombre
Licencia: MIT
Datos meteorológicos: OpenWeatherMap (https://openweathermap.org)
Datos geográficos: ESRI/IGN España
"""

import json
import requests
from datetime import datetime
import time
import os

# Configuración
OPENWEATHER_API_KEY = os.environ.get('OPENWEATHER_API_KEY')
GEOJSON_FILE = 'data/municipios_madrid.geojson'
OUTPUT_FILE = 'data/weather_data.json'

# Criterios para evaluar el "buen tiempo"
# Estos valores se pueden ajustar según tus preferencias
CRITERIOS = {
    'temp_optima_min': 15,      # Temperatura mínima ideal (°C)
    'temp_optima_max': 25,      # Temperatura máxima ideal (°C)
    'temp_precaucion_min': 8,   # Por debajo de esto, hace frío
    'temp_precaucion_max': 32,  # Por encima de esto, hace calor
    'viento_precaucion': 20,    # Viento en km/h que requiere precaución
    'viento_peligroso': 40,     # Viento peligroso en km/h
    'lluvia_ligera': 2,         # mm/h de lluvia ligera
    'lluvia_fuerte': 7.6        # mm/h de lluvia fuerte
}


def obtener_datos_clima(lat, lon, nombre_municipio):
    """
    Consulta la API de OpenWeatherMap para obtener datos meteorológicos
    de un municipio específico usando sus coordenadas.
    
    Args:
        lat: Latitud del municipio
        lon: Longitud del municipio
        nombre_municipio: Nombre del municipio (para logging)
    
    Returns:
        Diccionario con los datos meteorológicos o None si hay error
    """
    url = f"https://api.openweathermap.org/data/2.5/weather"
    params = {
        'lat': lat,
        'lon': lon,
        'appid': OPENWEATHER_API_KEY,
        'units': 'metric',  # Para obtener temperatura en Celsius
        'lang': 'es'        # Descripciones en español
    }
    
    try:
        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error al obtener datos para {nombre_municipio}: {e}")
        return None


def calcular_indice_tiempo(datos_clima):
    """
    Calcula el índice de "buen tiempo" basándose en múltiples variables
    meteorológicas. Devuelve un nivel (verde/amarillo/rojo) y consejos.
    
    Args:
        datos_clima: Diccionario con datos de OpenWeatherMap
    
    Returns:
        Diccionario con nivel, puntuación, y consejos
    """
    if not datos_clima:
        return {
            'nivel': 'sin-datos',
            'puntuacion': 0,
            'consejos': ['No hay datos disponibles'],
            'color': '#gray'
        }
    
    # Extraer variables meteorológicas
    temp = datos_clima['main']['temp']
    sensacion = datos_clima['main']['feels_like']
    humedad = datos_clima['main']['humidity']
    viento = datos_clima['wind']['speed'] * 3.6  # Convertir m/s a km/h
    
    # Lluvia (puede no estar presente si no llueve)
    lluvia = 0
    if 'rain' in datos_clima and '1h' in datos_clima['rain']:
        lluvia = datos_clima['rain']['1h']
    
    # Nieve (puede no estar presente)
    nieve = 0
    if 'snow' in datos_clima and '1h' in datos_clima['snow']:
        nieve = datos_clima['snow']['1h']
    
    # Sistema de puntuación (100 = perfecto, 0 = terrible)
    puntuacion = 100
    consejos = []
    
    # Evaluar temperatura
    if CRITERIOS['temp_optima_min'] <= temp <= CRITERIOS['temp_optima_max']:
        # Temperatura perfecta
        pass
    elif CRITERIOS['temp_precaucion_min'] <= temp < CRITERIOS['temp_optima_min']:
        puntuacion -= 20
        consejos.append('🧥 Hace algo de frío, lleva una chaqueta')
    elif CRITERIOS['temp_optima_max'] < temp <= CRITERIOS['temp_precaucion_max']:
        puntuacion -= 20
        consejos.append('☀️ Hace calor, lleva agua y protección solar')
    elif temp < CRITERIOS['temp_precaucion_min']:
        puntuacion -= 50
        consejos.append('❄️ Hace mucho frío, abrígate bien')
    else:  # temp > temp_precaucion_max
        puntuacion -= 50
        consejos.append('🌡️ Hace mucho calor, evita exposición prolongada')
    
    # Evaluar sensación térmica si es muy diferente a la temperatura real
    if abs(sensacion - temp) > 5:
        puntuacion -= 10
        if sensacion < temp:
            consejos.append('🌬️ El viento hace que se sienta más frío')
        else:
            consejos.append('💧 La humedad hace que se sienta más calor')
    
    # Evaluar viento
    if viento < CRITERIOS['viento_precaucion']:
        # Viento suave, ideal
        pass
    elif viento < CRITERIOS['viento_peligroso']:
        puntuacion -= 25
        consejos.append(f'💨 Viento moderado ({int(viento)} km/h), ten precaución')
    else:
        puntuacion -= 60
        consejos.append(f'⚠️ Viento fuerte ({int(viento)} km/h), peligroso para actividades')
    
    # Evaluar lluvia
    if lluvia == 0:
        # Sin lluvia, perfecto
        pass
    elif lluvia < CRITERIOS['lluvia_ligera']:
        puntuacion -= 20
        consejos.append('🌦️ Lluvia ligera, lleva paraguas')
    elif lluvia < CRITERIOS['lluvia_fuerte']:
        puntuacion -= 40
        consejos.append('☔ Lluvia moderada, mejor postponer actividades')
    else:
        puntuacion -= 70
        consejos.append('⛈️ Lluvia fuerte, no es buen momento para salir')
    
    # Evaluar nieve
    if nieve > 0:
        puntuacion -= 50
        consejos.append('🌨️ Está nevando, extrema precaución')
    
    # Si no hay consejos, significa que está perfecto
    if not consejos:
        consejos.append('✨ Condiciones perfectas para actividades al aire libre')
    
    # Determinar nivel según puntuación
    if puntuacion >= 70:
        nivel = 'verde'
        color = '#10b981'  # Verde
        mensaje_general = 'Excelente para salir'
    elif puntuacion >= 40:
        nivel = 'amarillo'
        color = '#f59e0b'  # Amarillo/Naranja
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


def procesar_municipios():
    """
    Función principal que lee el GeoJSON de municipios, obtiene datos
    meteorológicos para cada uno, y genera el archivo JSON de salida.
    """
    print("🚀 Iniciando actualización de datos meteorológicos...")
    print(f"⏰ Hora de inicio: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    # Verificar que existe la API key
    if not OPENWEATHER_API_KEY:
        print("❌ Error: No se encontró OPENWEATHER_API_KEY en las variables de entorno")
        return
    
    # Leer el archivo GeoJSON con los municipios
    try:
        with open(GEOJSON_FILE, 'r', encoding='utf-8') as f:
            geojson = json.load(f)
    except FileNotFoundError:
        print(f"❌ Error: No se encontró el archivo {GEOJSON_FILE}")
        return
    
    municipios_procesados = []
    total_municipios = len(geojson['features'])
    
    print(f"📍 Procesando {total_municipios} municipios...")
    
    for idx, feature in enumerate(geojson['features'], 1):
        # Obtener información del municipio
        properties = feature['properties']
        geometry = feature['geometry']
        
        # Calcular centroide del municipio para consultar el clima
        # Si es un Polygon, tomamos el primer conjunto de coordenadas
        if geometry['type'] == 'Polygon':
            coords = geometry['coordinates'][0]
        elif geometry['type'] == 'MultiPolygon':
            coords = geometry['coordinates'][0][0]
        else:
            print(f"⚠️ Geometría no soportada para {properties.get('NAMEUNIT', 'desconocido')}")
            continue
        
        # Calcular centroide simple (promedio de coordenadas)
        # Nota: las coordenadas GeoJSON están en formato [lon, lat]
        lons = [coord[0] for coord in coords]
        lats = [coord[1] for coord in coords]
        lon_centro = sum(lons) / len(lons)
        lat_centro = sum(lats) / len(lats)
        
        nombre = properties.get('NAMEUNIT', 'Desconocido')
        print(f"  [{idx}/{total_municipios}] Procesando {nombre}...")
        
        # Obtener datos meteorológicos
        datos_clima = obtener_datos_clima(lat_centro, lon_centro, nombre)
        
        if datos_clima:
            # Calcular índice de buen tiempo
            indice = calcular_indice_tiempo(datos_clima)
            
            # Preparar datos para guardar
            municipio_data = {
                'nombre': nombre,
                'codigo_ine': properties.get('NATCODE', ''),
                'coordenadas': {
                    'lat': lat_centro,
                    'lon': lon_centro
                },
                'clima': {
                    'temperatura': round(datos_clima['main']['temp'], 1),
                    'sensacion': round(datos_clima['main']['feels_like'], 1),
                    'humedad': datos_clima['main']['humidity'],
                    'viento': round(datos_clima['wind']['speed'] * 3.6, 1),  # km/h
                    'descripcion': datos_clima['weather'][0]['description'],
                    'icono': datos_clima['weather'][0]['icon']
                },
                'indice': indice,
                'geometry': geometry  # Guardar geometría para el mapa
            }
            
            municipios_procesados.append(municipio_data)
        
        # Pausa pequeña entre llamadas para no saturar la API
        # (60 llamadas por minuto es el límite del plan gratuito)
        time.sleep(1)
    
    # Preparar datos finales con metadata
    datos_finales = {
        'metadata': {
            'ultima_actualizacion': datetime.now().isoformat(),
            'ultima_actualizacion_formateada': datetime.now().strftime('%d/%m/%Y a las %H:%M'),
            'total_municipios': len(municipios_procesados),
            'fuente_clima': 'OpenWeatherMap',
            'fuente_geodatos': 'ESRI/IGN España'
        },
        'municipios': municipios_procesados
    }
    
    # Guardar en archivo JSON
    with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
        json.dump(datos_finales, f, ensure_ascii=False, indent=2)
    
    print(f"\n✅ Proceso completado exitosamente!")
    print(f"📊 {len(municipios_procesados)} municipios procesados")
    print(f"💾 Datos guardados en: {OUTPUT_FILE}")
    print(f"⏰ Hora de finalización: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")


if __name__ == "__main__":
    procesar_municipios()
