# Changelog

Todos los cambios notables en este proyecto serán documentados en este archivo.

El formato está basado en [Keep a Changelog](https://keepachangelog.com/es-ES/1.0.0/),
y este proyecto adhiere a [Versionado Semántico](https://semver.org/lang/es/).

## [No publicado]

### Por implementar
- Alertas de calidad del aire para zonas específicas de Madrid
- Visualización de islas de calor urbanas en diferentes distritos
- Predicciones de eventos climáticos extremos (olas de calor, tormentas)
- Recomendaciones de rutas más frescas en días de altas temperaturas

## [0.2.0] - 2025-01-12

### Añadido
- **Integración de Google Analytics con privacidad mejorada**: Implementado sistema de analítica web para comprender mejor cómo los madrileños utilizan la aplicación y qué funcionalidades relacionadas con datos meteorológicos y ambientales son más relevantes para ellos.
  - Configuración con anonimización de IP activada mediante parámetro `anonymize_ip: true`
  - Desactivación de Google Signals para evitar seguimiento entre dispositivos (`allow_google_signals: false`)
  - Desactivación de personalización de anuncios (`allow_ad_personalization_signals: false`)
  - Retención de datos configurada al mínimo legal (2 meses)
  - Solo se recopilan estadísticas agregadas y anónimas
  - Seguimiento de eventos clave de interacción con el mapa
  - Métricas de uso que permitirán priorizar mejoras futuras enfocadas en necesidades reales de la comunidad madrileña
- **Política de Privacidad completa**: Nuevo archivo PRIVACY.md que explica de forma clara y transparente cómo se manejan los datos de los usuarios.
  - Descripción detallada de qué datos se recopilan y qué NO se recopila
  - Explicación sobre anonimización de direcciones IP
  - Guía para usuarios que deseen desactivar completamente el rastreo
  - Información sobre retención de datos y derechos de los usuarios
  - Cumplimiento con RGPD y LOPD española
- **Enlace visible a la Política de Privacidad**: Añadido enlace discreto en el footer de la aplicación para que los usuarios puedan consultar fácilmente cómo se manejan sus datos.
- **Enlace al código fuente**: Añadido enlace al repositorio de GitHub en el footer para promover la transparencia y permitir que cualquiera pueda auditar el código.

### Mejorado
- **Documentación del README**: Actualizado con sección dedicada a privacidad y protección de datos, explicando el compromiso del proyecto con la privacidad de los usuarios madrileños.
- **Transparencia del proyecto**: Todo el manejo de datos de usuario está ahora documentado públicamente y es auditable.
- **Estructura del footer**: Reorganizado para incluir enlaces a recursos importantes (código fuente y privacidad) de forma discreta pero accesible.
- Optimización del rendimiento de carga del mapa
- Mejora en la presentación visual del footer con separadores y hover effects

## [0.1.0] - 2025-01-04

### Añadido
- Lanzamiento inicial de Madrid Weather Map
- Visualización interactiva de datos meteorológicos de Madrid
- Mapa base con información climática en tiempo real
- Interfaz responsiva adaptada a dispositivos móviles y escritorio
- Integración con servicios de datos meteorológicos
- Enfoque específico en la ciudad de Madrid y sus particularidades climáticas urbanas

### Características principales
- Visualización geoespacial de condiciones meteorológicas actuales
- Interfaz intuitiva para ciudadanos madrileños preocupados por el medio ambiente
- Datos actualizados sobre temperatura, humedad y condiciones generales del clima
- Diseño limpio enfocado en la usabilidad

---

## Convenciones de este Changelog

### Tipos de cambios
- **Añadido**: Para nuevas funcionalidades
- **Cambiado**: Para cambios en funcionalidades existentes
- **Obsoleto**: Para funcionalidades que serán eliminadas próximamente
- **Eliminado**: Para funcionalidades eliminadas
- **Corregido**: Para corrección de errores
- **Seguridad**: Para vulnerabilidades de seguridad corregidas
- **Mejorado**: Para mejoras en rendimiento o experiencia de usuario
