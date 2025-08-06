#!/usr/bin/env python3
"""
Script para generar certificados SSL autofirmados para desarrollo local
"""
import os
import subprocess
import sys

def generate_ssl_certificates():
    """Genera certificados SSL autofirmados"""
    
    # Crear directorio ssl si no existe
    if not os.path.exists('ssl'):
        os.makedirs('ssl')
    
    # Configuración del certificado
    cert_config = """[req]
distinguished_name = req_distinguished_name
x509_extensions = v3_req
prompt = no

[req_distinguished_name]
C = MX
ST = Mexico
L = Ciudad
O = Emergency GPS
OU = Development
CN = localhost

[v3_req]
keyUsage = keyEncipherment, dataEncipherment
extendedKeyUsage = serverAuth
subjectAltName = @alt_names

[alt_names]
DNS.1 = localhost
DNS.2 = *.localhost
IP.1 = 127.0.0.1
IP.2 = 0.0.0.0
"""
    
    # Escribir configuración temporal
    with open('ssl/cert.conf', 'w') as f:
        f.write(cert_config)
    
    try:
        # Generar clave privada
        subprocess.run([
            'openssl', 'genrsa', '-out', 'ssl/key.pem', '2048'
        ], check=True)
        
        # Generar certificado
        subprocess.run([
            'openssl', 'req', '-new', '-x509', '-key', 'ssl/key.pem',
            '-out', 'ssl/cert.pem', '-days', '365',
            '-config', 'ssl/cert.conf'
        ], check=True)
        
        print("✅ Certificados SSL generados exitosamente:")
        print("   - ssl/cert.pem (certificado)")
        print("   - ssl/key.pem (clave privada)")
        
        # Limpiar archivo temporal
        os.remove('ssl/cert.conf')
        
        return True
        
    except subprocess.CalledProcessError as e:
        print(f"❌ Error generando certificados: {e}")
        return False
    except FileNotFoundError:
        print("❌ OpenSSL no encontrado. Instalando...")
        return install_openssl_and_retry()

def install_openssl_and_retry():
    """Intenta instalar OpenSSL y generar certificados"""
    try:
        # Para Windows con chocolatey
        if os.name == 'nt':
            print("Instalando OpenSSL con chocolatey...")
            subprocess.run(['choco', 'install', 'openssl', '-y'], check=True)
        else:
            print("Por favor instala OpenSSL manualmente")
            return False
            
        return generate_ssl_certificates()
    except:
        print("❌ No se pudo instalar OpenSSL automáticamente")
        print("💡 Solución alternativa: usar certificados pre-generados")
        return generate_fallback_certificates()

def generate_fallback_certificates():
    """Genera certificados usando Python (menos seguro pero funcional)"""
    try:
        from cryptography import x509
        from cryptography.x509.oid import NameOID
        from cryptography.hazmat.primitives import hashes
        from cryptography.hazmat.primitives.asymmetric import rsa
        from cryptography.hazmat.primitives import serialization
        import datetime
        
        # Generar clave privada
        private_key = rsa.generate_private_key(
            public_exponent=65537,
            key_size=2048,
        )
        
        # Crear certificado
        subject = issuer = x509.Name([
            x509.NameAttribute(NameOID.COUNTRY_NAME, "MX"),
            x509.NameAttribute(NameOID.STATE_OR_PROVINCE_NAME, "Mexico"),
            x509.NameAttribute(NameOID.LOCALITY_NAME, "Ciudad"),
            x509.NameAttribute(NameOID.ORGANIZATION_NAME, "Emergency GPS"),
            x509.NameAttribute(NameOID.COMMON_NAME, "localhost"),
        ])
        
        cert = x509.CertificateBuilder().subject_name(
            subject
        ).issuer_name(
            issuer
        ).public_key(
            private_key.public_key()
        ).serial_number(
            x509.random_serial_number()
        ).not_valid_before(
            datetime.datetime.utcnow()
        ).not_valid_after(
            datetime.datetime.utcnow() + datetime.timedelta(days=365)
        ).add_extension(
            x509.SubjectAlternativeName([
                x509.DNSName("localhost"),
                x509.IPAddress(ipaddress.IPv4Address("127.0.0.1")),
            ]),
            critical=False,
        ).sign(private_key, hashes.SHA256())
        
        # Guardar certificado
        with open("ssl/cert.pem", "wb") as f:
            f.write(cert.public_bytes(serialization.Encoding.PEM))
        
        # Guardar clave privada
        with open("ssl/key.pem", "wb") as f:
            f.write(private_key.private_bytes(
                encoding=serialization.Encoding.PEM,
                format=serialization.PrivateFormat.PKCS8,
                encryption_algorithm=serialization.NoEncryption()
            ))
        
        print("✅ Certificados SSL generados con Python:")
        print("   - ssl/cert.pem (certificado)")
        print("   - ssl/key.pem (clave privada)")
        
        return True
        
    except ImportError:
        print("❌ Librería cryptography no disponible")
        print("💡 Instalando cryptography...")
        subprocess.run([sys.executable, '-m', 'pip3', 'install', 'cryptography'])
        return generate_fallback_certificates()
    except Exception as e:
        print(f"❌ Error generando certificados con Python: {e}")
        return False

if __name__ == "__main__":
    print("🔐 Generando certificados SSL para HTTPS...")
    success = generate_ssl_certificates()
    
    if success:
        print("\n🚀 Ahora puedes ejecutar la aplicación con HTTPS:")
        print("   docker-compose up --build")
        print("\n🌐 Accede a: https://localhost:5000")
        print("\n⚠️  Tu navegador mostrará una advertencia de seguridad.")
        print("   Haz click en 'Avanzado' → 'Continuar a localhost'")
    else:
        print("\n❌ No se pudieron generar los certificados SSL")
        print("💡 La aplicación funcionará en HTTP pero la geolocalización puede fallar")