from flask import Flask, render_template, request, jsonify
import requests
import os
from datetime import datetime
from dotenv import load_dotenv
from twilio.rest import Client

load_dotenv()

app = Flask(__name__)

# Configuración de Twilio para WhatsApp
TWILIO_ACCOUNT_SID = os.getenv('TWILIO_ACCOUNT_SID')
TWILIO_AUTH_TOKEN = os.getenv('TWILIO_AUTH_TOKEN')
TWILIO_WHATSAPP_NUMBER = os.getenv('TWILIO_WHATSAPP_NUMBER')  # ej: whatsapp:+14155238886
EMERGENCY_CONTACT = os.getenv('EMERGENCY_CONTACT')  # ej: whatsapp:+1234567890

@app.route('/')
def index():
    return render_template('index.html')

# Variable global para tracking de heartbeat
last_heartbeat = datetime.now()
heartbeat_active = False

@app.route('/send_emergency_alert', methods=['POST'])
def send_emergency_alert():
    try:
        data = request.json
        latitude = data.get('latitude')
        longitude = data.get('longitude')
        alert_type = data.get('type', 'manual')  # manual o auto
        
        if not latitude or not longitude:
            return jsonify({'error': 'Coordenadas no proporcionadas'}), 400
        
        # Obtener dirección aproximada usando geocodificación inversa
        address = get_address_from_coordinates(latitude, longitude)
        
        # Crear mensaje de emergencia
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        google_maps_link = f"https://maps.google.com/?q={latitude},{longitude}"
        
        if alert_type == 'auto':
            message = f"""⚠️ ALERTA AUTOMÁTICA - POSIBLE EMERGENCIA ⚠️
            
DISPOSITIVO DESCONECTADO INESPERADAMENTE

Fecha y hora: {timestamp}
Última ubicación conocida: {address}
Coordenadas: {latitude}, {longitude}
Ver en mapa: {google_maps_link}

El dispositivo se desconectó del sistema de emergencia. Por favor, verifica el estado de la persona inmediatamente."""
        else:
            message = f"""🚨 ALERTA DE EMERGENCIA 🚨
            
Fecha y hora: {timestamp}
Ubicación: {address}
Coordenadas: {latitude}, {longitude}
Ver en mapa: {google_maps_link}

Esta es una alerta manual de emergencia. Por favor, verifica mi estado inmediatamente."""
        
        # Enviar mensaje por WhatsApp
        success = send_whatsapp_message(message)
        
        if success:
            return jsonify({'success': True, 'message': 'Alerta enviada correctamente'})
        else:
            return jsonify({'error': 'Error al enviar la alerta'}), 500
            
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/heartbeat', methods=['POST'])
def heartbeat():
    global last_heartbeat, heartbeat_active
    data = request.json
    last_heartbeat = datetime.now()
    heartbeat_active = True
    
    # Guardar última ubicación conocida
    if data.get('latitude') and data.get('longitude'):
        app.config['last_location'] = {
            'latitude': data['latitude'],
            'longitude': data['longitude'],
            'timestamp': last_heartbeat
        }
    
    return jsonify({'status': 'ok'})

@app.route('/start_monitoring', methods=['POST'])
def start_monitoring():
    global heartbeat_active
    heartbeat_active = True
    return jsonify({'status': 'monitoring started'})

@app.route('/stop_monitoring', methods=['POST'])
def stop_monitoring():
    global heartbeat_active
    heartbeat_active = False
    return jsonify({'status': 'monitoring stopped'})

def get_address_from_coordinates(lat, lon):
    try:
        # Usar API gratuita de geocodificación inversa
        url = f"https://nominatim.openstreetmap.org/reverse?format=json&lat={lat}&lon={lon}&zoom=18&addressdetails=1"
        headers = {'User-Agent': 'EmergencyGPS/1.0'}
        response = requests.get(url, headers=headers)
        
        if response.status_code == 200:
            data = response.json()
            return data.get('display_name', f"Lat: {lat}, Lon: {lon}")
        else:
            return f"Lat: {lat}, Lon: {lon}"
    except:
        return f"Lat: {lat}, Lon: {lon}"

def send_whatsapp_message(message):
    try:
        if not all([TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN, TWILIO_WHATSAPP_NUMBER, EMERGENCY_CONTACT]):
            print("Configuración de Twilio incompleta")
            return False
            
        client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)
        
        message = client.messages.create(
            body=message,
            from_=TWILIO_WHATSAPP_NUMBER,
            to=EMERGENCY_CONTACT
        )
        
        print(f"Mensaje enviado: {message.sid}")
        return True
        
    except Exception as e:
        print(f"Error enviando WhatsApp: {e}")
        return False

# Función para monitorear heartbeat en segundo plano
def monitor_heartbeat():
    import threading
    import time
    
    def check_heartbeat():
        global last_heartbeat, heartbeat_active
        while True:
            time.sleep(30)  # Revisar cada 30 segundos
            
            if heartbeat_active:
                time_diff = (datetime.now() - last_heartbeat).total_seconds()
                
                # Si no hay heartbeat por más de 2 minutos, enviar alerta
                if time_diff > 120:
                    print(f"⚠️ Heartbeat perdido por {time_diff} segundos")
                    
                    # Obtener última ubicación conocida
                    last_location = app.config.get('last_location')
                    if last_location:
                        # Simular request para enviar alerta automática
                        with app.app_context():
                            try:
                                address = get_address_from_coordinates(
                                    last_location['latitude'], 
                                    last_location['longitude']
                                )
                                
                                timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                                google_maps_link = f"https://maps.google.com/?q={last_location['latitude']},{last_location['longitude']}"
                                
                                message = f"""⚠️ ALERTA AUTOMÁTICA - POSIBLE EMERGENCIA ⚠️
                                
DISPOSITIVO DESCONECTADO INESPERADAMENTE

Fecha y hora: {timestamp}
Última ubicación conocida: {address}
Coordenadas: {last_location['latitude']}, {last_location['longitude']}
Ver en mapa: {google_maps_link}
Última conexión: {last_location['timestamp'].strftime("%Y-%m-%d %H:%M:%S")}

El dispositivo se desconectó del sistema de emergencia. Por favor, verifica el estado de la persona inmediatamente."""
                                
                                send_whatsapp_message(message)
                                print("✅ Alerta automática enviada por desconexión")
                                
                            except Exception as e:
                                print(f"❌ Error enviando alerta automática: {e}")
                    
                    # Desactivar monitoring hasta que se reconecte
                    heartbeat_active = False
    
    # Iniciar thread de monitoreo
    monitor_thread = threading.Thread(target=check_heartbeat, daemon=True)
    monitor_thread.start()

if __name__ == '__main__':
    # Inicializar configuración
    app.config['last_location'] = None
    
    # Iniciar monitoreo de heartbeat
    monitor_heartbeat()
    
    app.run(host='0.0.0.0', port=5000, debug=True)