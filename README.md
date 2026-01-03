# 🌤️ Madrid Weather Map - ¿Hace buen tiempo hoy?

Un mapa interactivo que muestra el tiempo actualizado en cada municipio de la Comunidad de Madrid, ayudándote a decidir si es buen momento para actividades al aire libre.

[![Actualización automática](https://github.com/TrueRomanZe/madrid-weather-map/actions/workflows/update-weather.yml/badge.svg)](https://github.com/TrueRomanZe/madrid-weather-map/actions/workflows/update-weather.yml)

## 🎯 ¿Qué hace este proyecto?

Este proyecto te permite visualizar de un vistazo si hace buen tiempo en tu municipio de la Comunidad de Madrid. Utilizando un sistema de colores intuitivo (verde, amarillo, rojo), puedes saber inmediatamente si es un buen día para actividades al aire libre.

### Sistema de clasificación por colores

- **🟢 Verde**: Condiciones perfectas para salir y hacer actividades al aire libre
- **🟡 Amarillo**: Condiciones aceptables, pero toma algunas precauciones
- **🔴 Rojo**: Mejor quedarse en casa por condiciones meteorológicas adversas

El sistema analiza múltiples variables meteorológicas (temperatura, sensación térmica, viento, lluvia y nieve) para darte una recomendación personalizada y consejos específicos para cada municipio.

## ✨ Características principales

- 🗺️ **Mapa interactivo** con los 179 municipios de la Comunidad de Madrid coloreados según las condiciones meteorológicas
- 🔍 **Buscador inteligente** que encuentra municipios escribiendo solo parte del nombre (ej: "Alcalá" encuentra "Alcalá de Henares")
- 📊 **Datos actualizados** automáticamente cada 3 horas mediante GitHub Actions
- 💡 **Consejos personalizados** para cada municipio según las condiciones específicas del momento
- 📱 **Diseño responsive** que funciona perfectamente en móviles, tablets y ordenadores
- 🎨 **Interfaz moderna** y atractiva con animaciones suaves y colores vibrantes
- ⚡ **Sin instalación necesaria** - funciona directamente en el navegador
- 🆓 **Completamente gratuito** y de código abierto

## 🚀 Ver el proyecto en vivo

Visita: [https://TrueromanZe.github.io/madrid-weather-map](https://TrueRomanZe.github.io/madrid-weather-map)

*(Reemplaza con tu URL real una vez publicado el proyecto en GitHub Pages)*

## 🛠️ Tecnologías utilizadas

Este proyecto combina diferentes tecnologías modernas para crear una experiencia fluida y fiable:

### Backend y automatización
- **Python 3.11** - Lenguaje de programación para el script de procesamiento
- **Requests** - Biblioteca para realizar peticiones HTTP a la API
- **GitHub Actions** - Plataforma de automatización que ejecuta el script cada 3 horas

### Frontend
- **HTML5/CSS3** - Estructura y diseño de la página web
- **JavaScript (ES6+)** - Lógica de la aplicación y gestión del mapa
- **Leaflet.js 1.9.4** - Biblioteca líder para mapas interactivos en la web

### Datos y servicios
- **OpenWeatherMap API** - Proveedor de datos meteorológicos en tiempo real
- **OpenStreetMap** - Mapa base de alta calidad y código abierto
- **GitHub Pages** - Servicio de hosting gratuito para sitios estáticos

## 📊 Fuentes de datos y créditos

### Datos meteorológicos
Los datos del tiempo provienen de [OpenWeatherMap](https://openweathermap.org/), un servicio que proporciona información meteorológica precisa y actualizada para cualquier ubicación del mundo. La API se consulta cada 3 horas para mantener los datos frescos sin exceder los límites del plan gratuito.

### Datos geográficos
Los límites administrativos de los municipios de la Comunidad de Madrid provienen de fuentes oficiales:
- **ESRI España** - [Living Atlas](https://livingatlas.arcgis.com/)
- **Instituto Geográfico Nacional (IGN)** - [www.ign.es](https://www.ign.es/)

Estos datos oficiales garantizan que los límites municipales sean precisos y estén actualizados según las divisiones administrativas oficiales.

### Mapa base
El mapa base proviene de [OpenStreetMap](https://www.openstreetmap.org/), un proyecto colaborativo de cartografía libre que crea un mapa del mundo de código abierto y editable, mantenido por una comunidad de voluntarios.

## 🧮 ¿Cómo se calcula el "buen tiempo"?

El sistema evalúa múltiples factores meteorológicos y asigna una puntuación de 0 a 100 a cada municipio. La puntuación comienza en 100 (perfecta) y se va reduciendo según los factores adversos detectados.

### Factores evaluados en detalle

**Temperatura ambiente**
- Rango óptimo: 15°C - 25°C (sin penalización)
- Rango aceptable: 8°C - 15°C o 25°C - 32°C (penalización leve)
- Temperaturas extremas: Por debajo de 8°C o por encima de 32°C (penalización severa)

**Sensación térmica**
Si la sensación térmica difiere más de 5°C de la temperatura real debido al viento o la humedad, se aplica una penalización adicional para alertar al usuario.

**Velocidad del viento**
- Brisa suave: Menos de 20 km/h (ideal)
- Viento moderado: 20-40 km/h (requiere precaución)
- Viento fuerte: Más de 40 km/h (peligroso)

**Precipitación**
- Sin lluvia: Condiciones ideales
- Lluvia ligera: Menos de 2 mm/h (paraguas recomendado)
- Lluvia moderada: 2-7.6 mm/h (mejor postponer actividades)
- Lluvia fuerte: Más de 7.6 mm/h (quedarse en casa)

**Nieve**
Cualquier cantidad de nieve activa una alerta especial por las condiciones resbaladizas que genera.

### Sistema de clasificación final

La puntuación total determina el color y la recomendación:

- **🟢 Verde (70-100 puntos)**: Condiciones óptimas para actividades al aire libre. ¡Es un gran día para salir!
- **🟡 Amarillo (40-69 puntos)**: Condiciones aceptables con precauciones. Puedes salir pero prepárate adecuadamente.
- **🔴 Rojo (0-39 puntos)**: Condiciones adversas. Mejor quedarse en casa o limitar el tiempo al aire libre.

Además de la clasificación por color, el sistema genera consejos específicos para cada municipio basándose en las condiciones particulares detectadas.

## 🔧 Instalación y uso local

Si quieres ejecutar este proyecto en tu propio ordenador para desarrollo o personalización, sigue estos pasos.

### Requisitos previos

Antes de comenzar, asegúrate de tener instalado:
- **Python 3.11 o superior** - [Descargar Python](https://www.python.org/downloads/)
- **Git** - [Descargar Git](https://git-scm.com/downloads)
- **Una API key de OpenWeatherMap** - [Obtener API key gratuita](https://openweathermap.org/api)

### Pasos de instalación

#### 1. Clonar el repositorio
```bash
git clone https://github.com/TU-USUARIO/NOMBRE-REPO.git
cd NOMBRE-REPO
```

#### 2. Instalar las dependencias de Python
```bash
pip install requests
```

#### 3. Configurar tu API key de OpenWeatherMap

En **Windows (PowerShell)**:
```powershell
$env:OPENWEATHER_API_KEY="tu-api-key-aqui"
```

En **Windows (CMD)**:
```cmd
set OPENWEATHER_API_KEY=tu-api-key-aqui
```

En **Mac/Linux**:
```bash
export OPENWEATHER_API_KEY="tu-api-key-aqui"
```

#### 4. Ejecutar el script de actualización
```bash
python update_weather.py
```

El script consultará la API de OpenWeatherMap para todos los municipios y generará el archivo `data/weather_data.json` con los datos actualizados.

#### 5. Ver el mapa en tu navegador

Simplemente abre el archivo `index.html` en tu navegador web favorito. El mapa cargará automáticamente los datos del archivo JSON que acabas de generar.

## 📁 Estructura del proyecto

```
madrid-weather-map/
│
├── .github/
│   └── workflows/
│       └── update-weather.yml    # Configuración de GitHub Actions
│
├── data/
│   ├── municipios_madrid.geojson # Límites geográficos de municipios (GeoJSON)
│   └── weather_data.json         # Datos meteorológicos actualizados automáticamente
│
├── index.html                    # Página web principal (visualización del mapa)
├── update_weather.py             # Script Python de actualización de datos
├── README.md                     # Este archivo de documentación
└── LICENSE                       # Licencia MIT del proyecto
```

### Descripción de archivos clave

**update_weather.py**: Este es el corazón del proyecto. El script lee el archivo GeoJSON con los municipios, calcula el centroide de cada uno, consulta la API de OpenWeatherMap, evalúa las condiciones meteorológicas según criterios predefinidos, y genera el archivo JSON con toda la información procesada. Está extensamente documentado para facilitar su comprensión y modificación.

**index.html**: Página web autónoma que contiene todo el código HTML, CSS y JavaScript necesario para mostrar el mapa interactivo. Utiliza Leaflet.js para renderizar el mapa y gestionar las interacciones del usuario.

**.github/workflows/update-weather.yml**: Archivo de configuración que le dice a GitHub Actions cuándo y cómo ejecutar el script de Python. Está configurado para ejecutarse automáticamente cada 3 horas y también puede ejecutarse manualmente.

## 🤝 Contribuciones

Las contribuciones son bienvenidas y apreciadas. Si quieres mejorar este proyecto, hay varias formas de hacerlo.

### Formas de contribuir

- **Reportar bugs**: Si encuentras algún error, abre un issue describiendo el problema
- **Sugerir mejoras**: ¿Tienes ideas para nuevas funcionalidades? Compártelas en un issue
- **Mejorar la documentación**: Ayuda a hacer el proyecto más accesible mejorando la documentación
- **Contribuir código**: Implementa nuevas características o correcciones

### Proceso para contribuir con código

Si quieres contribuir código, sigue estos pasos:

1. Haz un fork del repositorio haciendo clic en el botón "Fork" en GitHub
2. Clona tu fork a tu ordenador local
   ```bash
   git clone https://github.com/tu-usuario/madrid-weather-map.git
   ```
3. Crea una rama para tu característica o corrección
   ```bash
   git checkout -b feature/nombre-descriptivo
   ```
4. Realiza tus cambios y haz commits descriptivos
   ```bash
   git commit -m 'Añadir: descripción clara de los cambios'
   ```
5. Sube tus cambios a tu fork
   ```bash
   git push origin feature/nombre-descriptivo
   ```
6. Abre un Pull Request desde tu fork hacia el repositorio original

### Guías de estilo para contribuciones

- **Código Python**: Sigue PEP 8 y añade docstrings descriptivos
- **Código JavaScript**: Usa ES6+ y comentarios claros
- **Commits**: Mensajes descriptivos en presente ("Añadir función" no "Añadida función")

## 📝 Licencia y términos de uso

### Licencia del proyecto
Este proyecto está bajo la **Licencia MIT**. Esto significa que puedes usar, copiar, modificar, fusionar, publicar, distribuir, sublicenciar y/o vender copias del software libremente. Ver el archivo [LICENSE](LICENSE) para los términos completos.

### Atribuciones obligatorias

Aunque el código de este proyecto es de código abierto, utiliza datos y servicios de terceros que tienen sus propias licencias y requisitos de atribución.

#### Datos meteorológicos
- **Proveedor**: OpenWeatherMap
- **Licencia**: Los datos están sujetos a los términos de uso de OpenWeatherMap
- **Atribución requerida**: Este proyecto debe mencionar que usa datos de OpenWeatherMap
- **Más información**: [OpenWeatherMap Terms](https://openweathermap.org/terms)

#### Datos geográficos
- **Proveedores**: ESRI Living Atlas / Instituto Geográfico Nacional de España
- **Licencia**: Los datos geográficos oficiales de España son de dominio público según la legislación española
- **Atribución requerida**: Se debe mencionar a ESRI/IGN como fuente de los datos geográficos

#### Mapas base
- **Proveedor**: OpenStreetMap
- **Licencia**: Open Database License (ODbL)
- **Atribución requerida**: © OpenStreetMap contributors
- **Más información**: [OpenStreetMap Copyright](https://www.openstreetmap.org/copyright)

#### Bibliotecas de software
- **Leaflet.js**: BSD-2-Clause License - [Leaflet](https://leafletjs.com/)
- **Requests (Python)**: Apache 2.0 License - [Requests](https://requests.readthedocs.io/)

## ⚠️ Aviso legal (Disclaimer)

Este proyecto es una herramienta informativa y educativa. **No debe usarse como única fuente para tomar decisiones críticas relacionadas con la seguridad o la salud**.

- Los datos meteorológicos provienen de una API de terceros y pueden contener imprecisiones
- El sistema de clasificación (verde/amarillo/rojo) es una simplificación y no sustituye el juicio personal
- Para alertas meteorológicas oficiales, consulta siempre la [Agencia Estatal de Meteorología (AEMET)](https://www.aemet.es/)
- En caso de condiciones meteorológicas extremas, sigue las recomendaciones de las autoridades locales

Los desarrolladores de este proyecto no se hacen responsables de cualquier daño o perjuicio derivado del uso de esta herramienta.

## 🔮 Desarrollo futuro

Ideas y características planeadas para futuras versiones:

- 📈 Histórico de datos meteorológicos con gráficos de tendencias
- 🌡️ Comparador entre municipios para planificar excursiones
- 🔔 Sistema de notificaciones para condiciones meteorológicas favorables
- 🎯 Recomendaciones personalizadas según tipo de actividad (running, ciclismo, picnic, etc.)
- 🌍 Expansión a otras comunidades autónomas de España
- 📱 Versión PWA (Progressive Web App) para uso offline

Si te interesa contribuir a alguna de estas características, ¡no dudes en abrir un issue o pull request!

## 📧 Contacto y soporte

Si tienes preguntas, sugerencias o encuentras algún problema:

- **Issues**: Abre un issue en este repositorio para reportar bugs o sugerir mejoras
- **Discusiones**: Usa la pestaña "Discussions" para preguntas generales o ideas
- **Email**: s.romera92@gmail.com

## 🙏 Agradecimientos

Este proyecto no sería posible sin:

- La comunidad de OpenStreetMap por mantener un mapa del mundo libre y actualizado
- OpenWeatherMap por proporcionar una API meteorológica accesible y fiable
- ESRI e IGN España por los datos geográficos oficiales
- La comunidad de código abierto por las herramientas y bibliotecas utilizadas
- Todos los contribuidores que ayudan a mejorar este proyecto

---

**Desarrollado con ❤️ para la Comunidad de Madrid**

*Última actualización del README: Enero 2026*
