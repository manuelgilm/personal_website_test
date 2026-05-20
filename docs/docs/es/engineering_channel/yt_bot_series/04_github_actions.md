# Serie 4: GitHub Actions - La Forma DevOps

## 🎯 Enfoque: Automatizando la Ejecución

Tu bot funciona muy bien cuando lo ejecutas manualmente, pero la verdadera automatización significa que se ejecuta según un cronograma sin intervención. ¡Configuraremos GitHub Actions para hacerlo realidad!

## 📚 Temas Cubiertos

### Escribiendo Flujos de Trabajo YAML
- Entender la estructura de GitHub Actions
- Disparadores (cronograma, en-push, manual, etc.)
- Definiciones de trabajos y pasos
- Usar acciones del mercado

### Gestionando Secretos de Forma Segura
- Almacenar claves API y credenciales de forma segura
- Bóveda de Secretos de GitHub
- Acceder a secretos en tus flujos de trabajo
- Mejores prácticas para gestión de secretos

### Configurando Trabajos Cron
- Programar tu bot para que se ejecute en momentos específicos
- Sintaxis de cron y cronometrización
- Ejecutar múltiples veces al día o en días específicos
- Manejar zonas horarias correctamente

### Manejo de Errores y Notificaciones
- Capturar y registrar errores en flujos de trabajo
- Enviar notificaciones en caso de fallo
- Estrategias de reintento
- Depuración de ejecuciones fallidas

## 🚀 Lo que Construirás

Al final de esta serie, tendrás:
- ✅ Un flujo de trabajo de GitHub Actions que ejecuta tu bot automáticamente
- ✅ Gestión segura de credenciales en tu pipeline de CI/CD
- ✅ Un bot que responde comentarios según un cronograma
- ✅ Notificaciones cuando algo sale mal

## 🔄 Arquitectura de Flujo de Trabajo

```
Disparador Programado (Cron)
    ↓
Verificar Repositorio
    ↓
Configurar Entorno Python
    ↓
Instalar Dependencias
    ↓
Ejecutar Script de Bot
    ↓
Registrar Resultados y Errores
    ↓
Notificar en Caso de Fallo
```

## 📝 Requisitos Previos

- Finalización de la Serie 3 (Ingeniería de Prompts y MLflow)
- Entendimiento básico de conceptos de CI/CD
- Conocimiento de Git y cuenta de GitHub

## 📋 Lista de Verificación de Flujo de Trabajo

- ✓ Crear directorio `.github/workflows/`
- ✓ Definir disparador de cronograma (cron)
- ✓ Configurar secretos para claves API
- ✓ Instalar dependencias
- ✓ Ejecutar bot con registro de MLflow
- ✓ Agregar manejo de errores y notificaciones

## 🎬 Mira y Sigue

Sigue el video para configurar tu primer flujo de trabajo automatizado. Usa esta guía para:
- Plantillas YAML de flujo de trabajo
- Configuración de secretos
- Ejemplos de expresiones de cron
- Solución de problemas de problemas comunes

## 💡 Expresiones Comunes de Cron

```
# Cada hora
0 * * * *

# Cada 6 horas
0 */6 * * *

# Cada día a las 9 AM UTC
0 9 * * *

# Cada lunes a las 8 AM UTC
0 8 * * 1

# Cada 30 minutos
*/30 * * * *
```

---

**Próximo Paso:** ¡Tu bot ahora está completamente automatizado! En la Serie 5, veremos el sistema completo end-to-end y agregaremos monitoreo y manejo de errores.