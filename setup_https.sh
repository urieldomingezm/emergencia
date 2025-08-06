#!/bin/bash

echo "🔐 Configurando HTTPS para Emergency GPS en Linux..."
echo ""

# Verificar si Python3 está instalado
if ! command -v python3 &> /dev/null; then
    echo "❌ Python3 no encontrado. Instalando..."
    
    # Detectar distribución Linux
    if command -v apt-get &> /dev/null; then
        # Ubuntu/Debian
        sudo apt-get update
        sudo apt-get install -y python3 python3-pip openssl
    elif command -v yum &> /dev/null; then
        # CentOS/RHEL
        sudo yum install -y python3 python3-pip openssl
    elif command -v dnf &> /dev/null; then
        # Fedora
        sudo dnf install -y python3 python3-pip openssl
    else
        echo "❌ No se pudo detectar el gestor de paquetes. Instala python3 manualmente."
        exit 1
    fi
fi

# Verificar si Docker está instalado
if ! command -v docker &> /dev/null; then
    echo "❌ Docker no encontrado. Instalando Docker..."
    
    # Instalar Docker
    curl -fsSL https://get.docker.com -o get-docker.sh
    sudo sh get-docker.sh
    sudo usermod -aG docker $USER
    
    echo "⚠️  Docker instalado. Reinicia tu sesión o ejecuta: newgrp docker"
fi

# Verificar si Docker Compose está instalado
if ! command -v docker-compose &> /dev/null; then
    echo "❌ Docker Compose no encontrado. Instalando..."
    
    # Instalar Docker Compose
    sudo curl -L "https://github.com/docker/compose/releases/latest/download/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
    sudo chmod +x /usr/local/bin/docker-compose
fi

echo "✅ Dependencias verificadas"
echo ""

# Generar certificados SSL
echo "🔐 Generando certificados SSL..."
python3 generate_ssl.py

echo ""
echo "🚀 Iniciando aplicación con HTTPS..."
echo "🌐 Accede a: https://localhost:5000"
echo "📱 En tu celular: https://[IP_DE_TU_SERVIDOR]:5000"
echo ""

# Mostrar IP del servidor
echo "📍 IPs disponibles:"
hostname -I | tr ' ' '\n' | grep -E '^[0-9]+\.[0-9]+\.[0-9]+\.[0-9]+$' | head -3 | while read ip; do
    echo "   https://$ip:5000"
done

echo ""
docker-compose up --build