# Sistema de Emergencia GPS con WhatsApp

Sistema web de geolocalización GPS para casos de emergencia que envía alertas automáticas por WhatsApp con tu ubicación exacta.

## 🚨 Características

- **Geolocalización automática**: Detecta tu ubicación GPS en tiempo real
- **Alertas por WhatsApp**: Envía mensajes automáticos a tu contacto de emergencia
- **Interfaz web responsive**: Funciona en móviles y computadoras
- **Dirección legible**: Convierte coordenadas GPS en direcciones comprensibles
- **Enlace a Google Maps**: Incluye link directo para ver la ubicación
- **Docker**: Fácil despliegue sin instalar Python

## 📋 Requisitos previos

1. **Docker Desktop** instalado en Windows
2. **Cuenta de Twilio** (gratuita) para envío de WhatsApp
3. **Navegador web** con soporte para geolocalización

## 🛠️ Configuración

### 1. Configurar Twilio para WhatsApp

1. Crea una cuenta gratuita en [Twilio](https://www.twilio.com/try-twilio)
2. Ve a la [Consola de Twilio](https://console.twilio.com/)
3. Obtén tu `Account SID` y `Auth Token`
4. Configura el Sandbox de WhatsApp en Twilio
5. Sigue las instrucciones para conectar tu número de WhatsApp

### 2. Configurar variables de entorno

Edita el archivo `.env` con tus datos reales:

```env
TWILIO_ACCOUNT_SID=tu_account_sid_real
TWILIO_AUTH_TOKEN=tu_auth_token_real
TWILIO_WHATSAPP_NUMBER=whatsapp:+14155238886
EMERGENCY_CONTACT=whatsapp:+521234567890
```

**Importante**: 
- `TWILIO_WHATSAPP_NUMBER` es el número de Twilio (generalmente +14155238886)
- `EMERGENCY_CONTACT` debe incluir el código de país (ej: +521234567890 para México)

## 🚀 Instalación y ejecución

### Opción 1: Con Docker (Recomendado)

```bash
# Construir la imagen
docker build -t emergency-gps .

# Ejecutar el contenedor
docker run -p 5000:5000 emergency-gps
```

### Opción 2: Con Docker Compose

```bash
# Crear y ejecutar
docker-compose up --build
```

## 📱 Uso

1. Abre tu navegador y ve a `http://localhost:5000`
2. Permite el acceso a tu ubicación cuando el navegador lo solicite
3. Espera a que se obtenga tu ubicación GPS
4. En caso de emergencia, presiona el botón rojo "ENVIAR ALERTA DE EMERGENCIA"
5. Confirma el envío en el diálogo que aparece
6. El sistema enviará automáticamente un mensaje de WhatsApp con:
   - Fecha y hora actual
   - Tu ubicación exacta (coordenadas y dirección)
   - Enlace directo a Google Maps
   - Mensaje de alerta de emergencia

## 📧 Ejemplo de mensaje de emergencia

```
🚨 ALERTA DE EMERGENCIA 🚨

Fecha y hora: 2025-01-15 14:30:25
Ubicación: Av. Insurgentes Sur 123, Ciudad de México
Coordenadas: 19.432608, -99.133209
Ver en mapa: https://maps.google.com/?q=19.432608,-99.133209

Esta es una alerta automática de emergencia. Por favor, verifica mi estado inmediatamente.
```

## 🔧 Personalización

### Cambiar el mensaje de emergencia
Edita la función `send_emergency_alert()` en `app.py` para personalizar el mensaje.

### Agregar más contactos
Modifica la función `send_whatsapp_message()` para enviar a múltiples contactos.

### Cambiar el diseño
Edita `templates/index.html` para personalizar la interfaz web.

## 🛡️ Seguridad

- Nunca compartas tu archivo `.env` 
- Mantén seguros tus tokens de Twilio
- Usa este sistema solo para emergencias reales
- Considera configurar límites de uso en Twilio

## 🆘 Solución de problemas

### Error: "Configuración de Twilio incompleta"
- Verifica que todas las variables en `.env` estén configuradas correctamente
- Asegúrate de que no haya espacios extra en los valores

### Error: "Acceso a ubicación denegado"
- Permite el acceso a ubicación en tu navegador
- Verifica que estés usando HTTPS o localhost

### Error al enviar WhatsApp
- Verifica que tu número esté registrado en el Sandbox de Twilio
- Confirma que el formato del número incluya el código de país

## 📞 Contactos de emergencia recomendados

- Familiares cercanos
- Servicios de emergencia locales
- Amigos de confianza
- Servicios médicos

## ⚠️ Advertencias importantes

- **Solo para emergencias reales**: No abuses del sistema
- **Batería del dispositivo**: Asegúrate de tener batería suficiente
- **Conexión a internet**: Requiere conexión estable para funcionar
- **Precisión GPS**: La precisión puede variar según las condiciones

## 🤝 Contribuciones

Las contribuciones son bienvenidas. Por favor:
1. Fork el proyecto
2. Crea una rama para tu feature
3. Commit tus cambios
4. Push a la rama
5. Abre un Pull Request

## 📄 Licencia

Este proyecto está bajo la Licencia MIT. Ver `LICENSE` para más detalles.