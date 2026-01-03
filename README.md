# 🌤️ Madrid Weather Map - ¿Hace buen tiempo hoy?

Un mapa interactivo que muestra el tiempo actualizado en cada municipio de la Comunidad de Madrid, ayudándote a decidir si es buen momento para actividades al aire libre.

## 🎯 ¿Qué hace este proyecto?

Este proyecto te permite visualizar de un vistazo si hace buen tiempo en tu municipio de la Comunidad de Madrid. Utilizando un sistema de colores intuitivo (verde, amarillo, rojo), puedes saber inmediatamente:

- **Verde**: Condiciones perfectas para salir y hacer actividades al aire libre
- **Amarillo**: Condiciones aceptables, pero toma algunas precauciones
- **Rojo**: Mejor quedarse en casa por condiciones meteorológicas adversas

El sistema analiza múltiples variables meteorológicas: temperatura, sensación térmica, viento, lluvia y nieve para darte una recomendación personalizada.

## ✨ Características

- 🗺️ **Mapa interactivo** con los 179 municipios de la Comunidad de Madrid
- 🔍 **Buscador inteligente** por nombre de municipio o código postal
- 📊 **Datos actualizados** cada 3 horas automáticamente
- 💡 **Consejos personalizados** para cada municipio según las condiciones
- 📱 **Diseño responsive** que funciona perfectamente en móviles y ordenadores
- 🎨 **Interfaz moderna** y atractiva con animaciones suaves

## 🚀 Ver el proyecto en vivo

Visita: [https://TU-USUARIO.github.io/NOMBRE-DE-TU-REPO](https://TU-USUARIO.github.io/NOMBRE-DE-TU-REPO)

*(Reemplaza con tu URL real una vez publicado)*

## 🛠️ Tecnologías utilizadas

- **Python 3.11** - Script de procesamiento de datos meteorológicos
- **GitHub Actions** - Automatización de actualizaciones cada 3 horas
- **Leaflet.js** - Biblioteca de mapas interactivos
- **OpenWeatherMap API** - Datos meteorológicos en tiempo real
- **OpenStreetMap** - Mapa base
- **HTML/CSS/JavaScript** - Frontend web

## 📊 Fuentes de datos

### Datos meteorológicos
Los datos del tiempo provienen de [OpenWeatherMap](https://openweathermap.org/), un servicio que proporciona información meteorológica actualizada y fiable.

### Datos geográficos
Los límites administrativos de los municipios de la Comunidad de Madrid provienen de:
- **ESRI España** - [Living Atlas](https://livingatlas.arcgis.com/)
- **Instituto Geográfico Nacional (IGN)** - [www.ign.es](https://www.ign.es/)

### Mapa base
El mapa base proviene de [OpenStreetMap](https://www.openstreetmap.org/), un proyecto colaborativo de cartografía libre.

## 🧮 ¿Cómo se calcula el "buen tiempo"?

El sistema evalúa múltiples factores meteorológicos y asigna una puntuación de 0 a 100 a cada municipio:

### Factores evaluados:
- **Temperatura**: Rango óptimo entre 15°C y 25°C
- **Sensación térmica**: Considera el efecto del viento y la humedad
- **Viento**: Velocidades superiores a 20 km/h requieren precaución
- **Precipitación**: Cualquier lluvia reduce la puntuación
- **Nieve**: Presencia de nieve activa alertas especiales

### Sistema de clasificación:
- **Verde (70-100 puntos)**: Condiciones óptimas para actividades al aire libre
- **Amarillo (40-69 puntos)**: Condiciones aceptables con precauciones
- **Rojo (0-39 puntos)**: Condiciones adversas, mejor quedarse en casa

## 🔧 Instalación local

Si quieres ejecutar este proyecto en tu ordenador:

### Requisitos previos
- Python 3.11 o superior
- Una API key de OpenWeatherMap (gratuita)
- Git

### Pasos

1. Clona el repositorio:
```bash
git clone https://github.com/TU-USUARIO/NOMBRE-DE-TU-REPO.git
cd NOMBRE-DE-TU-REPO
```

2. Instala las dependencias de Python:
```bash
pip install requests
```

3. Configura tu API key de OpenWeatherMap:
```bash
export OPENWEATHER_API_KEY="tu-api-key-aqui"
```

4. Ejecuta el script de actualización:
```bash
python update_weather.py
```

5. Abre `index.html` en tu navegador para ver el mapa.

## 📁 Estructura del proyecto

```
madrid-weather-map/
│
├── .github/
│   └── workflows/
│       └── update-weather.yml    # Configuración de GitHub Actions
│
├── data/
│   ├── municipios_madrid.geojson # Límites de municipios (GeoJSON)
│   └── weather_data.json         # Datos meteorológicos actualizados
│
├── update_weather.py             # Script Python de actualización
├── index.html                    # Página web principal
├── README.md                     # Este archivo
└── LICENSE                       # Licencia MIT
```

## 🤝 Contribuciones

Las contribuciones son bienvenidas. Si quieres mejorar este proyecto:

1. Haz un fork del repositorio
2. Crea una rama para tu característica (`git checkout -b feature/AmazingFeature`)
3. Haz commit de tus cambios (`git commit -m 'Add some AmazingFeature'`)
4. Haz push a la rama (`git push origin feature/AmazingFeature`)
5. Abre un Pull Request

## 📝 Créditos y Licencias

### Licencia del proyecto
Este proyecto está bajo la Licencia MIT. Ver el archivo [LICENSE](LICENSE) para más detalles.

### Atribuciones

#### Datos meteorológicos
- **OpenWeatherMap**: Los datos meteorológicos son proporcionados por OpenWeatherMap bajo su licencia de uso.
- Website: https://openweathermap.org/
- License: https://openweathermap.org/price

#### Datos geográficos
- **ESRI España / IGN**: Los límites administrativos de los municipios provienen de ESRI Living Atlas e IGN España.
- ESRI Living Atlas: https://livingatlas.arcgis.com/
- IGN España: https://www.ign.es/
- Los datos geográficos oficiales de España son de dominio público según la normativa española.

#### Mapas base
- **OpenStreetMap**: El mapa base es proporcionado por OpenStreetMap y sus colaboradores.
- Website: https://www.openstreetmap.org/
- License: © OpenStreetMap contributors, ODbL 1.0. https://www.openstreetmap.org/copyright

#### Bibliotecas de código
- **Leaflet.js**: Biblioteca de mapas interactivos (BSD-2-Clause License)
- Website: https://leafletjs.com/

## ⚠️ Disclaimer

Este proyecto es una herramienta informativa y no debe usarse como única fuente para tomar decisiones críticas relacionadas con la seguridad. Siempre consulta fuentes oficiales de meteorología (AEMET) para alertas y avisos importantes.

## 📧 Contacto

Si tienes preguntas o sugerencias, no dudes en abrir un issue en este repositorio.

---

Desarrollado con ❤️ para la Comunidad de Madrid
