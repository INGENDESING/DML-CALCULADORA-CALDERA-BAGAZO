# GUÍA DE DEPLOYMENT
# Calculadora de Caldera Acuotubular
## DML INGENIEROS CONSULTORES S.A.S.

---

## Tabla de Contenidos

1. [Consideraciones Generales](#1-consideraciones-generales)
2. [Deployment Local](#2-deployment-local)
3. [Deployment en Servidor Windows](#3-deployment-en-servidor-windows)
4. [Deployment en Servidor Linux](#4-deployment-en-servidor-linux)
5. [Deployment con Docker](#5-deployment-con-docker)
6. [Configuración de Producción](#6-configuración-de-producción)
7. [Monitoreo y Mantenimiento](#7-monitoreo-y-mantenimiento)

---

## 1. Consideraciones Generales

### 1.1 Arquitectura de la Aplicación

```
┌─────────────────────────────────────────────────────────────┐
│                     Navegador Web                           │
│              (Chrome, Firefox, Edge, Safari)                │
└──────────────────────────────┬──────────────────────────────┘
                               │ HTTP/HTTPS
                               ▼
┌─────────────────────────────────────────────────────────────┐
│                    Servidor Flask/Dash                      │
│                    (Puerto 8050/80)                         │
└──────────────────────────────┬──────────────────────────────┘
                               │
                               ▼
┌─────────────────────────────────────────────────────────────┐
│  Módulos Python:                                            │
│  - Termodinámica (IAPWS-97)                                 │
│  - Combustión                                               │
│  - Balance de Materia y Energía                             │
│  - Generación de PDF (ReportLab)                            │
└─────────────────────────────────────────────────────────────┘
```

### 1.2 Requisitos de Sistema

| Recurso | Mínimo | Recomendado |
|---------|--------|-------------|
| CPU | 2 núcleos | 4+ núcleos |
| RAM | 2 GB | 4+ GB |
| Disco | 500 MB | 2 GB |
| Python | 3.9+ | 3.11+ |
| Sistema | Win/macOS/Linux | Linux (Ubuntu 22.04+) |

---

## 2. Deployment Local

### 2.1 Instalación Rápida

```bash
# 1. Clonar o copiar el proyecto
cd "ruta/al/proyecto"

# 2. Crear entorno virtual (recomendado)
python -m venv venv

# 3. Activar entorno virtual
# Windows:
venv\Scripts\activate
# Linux/macOS:
source venv/bin/activate

# 4. Instalar dependencias
pip install -r requirements.txt

# 5. Ejecutar aplicación
python run.py
```

### 2.2 Verificación de Instalación

```bash
# Verificar versión de Python
python --version

# Verificar dependencias instaladas
pip list

# Ejecutar tests
python -m pytest app/tests/ -v
```

---

## 3. Deployment en Servidor Windows

### 3.1 Configuración como Servicio de Windows

Opción A: Usar NSSM (Non-Sucking Service Manager)

```bash
# 1. Descargar NSSM
# https://nssm.cc/download

# 2. Instalar el servicio
nssm install CalculadoraCaldera

# 3. Configurar:
#    - Path: C:\Python311\python.exe
#    - Startup directory: C:\ruta\al\proyecto
#    - Arguments: run.py --prod

# 4. Iniciar servicio
nssm start CalculadoraCaldera
```

Opción B: Usar Task Scheduler

1. Abrir "Task Scheduler"
2. Crear tarea básica
3. Trigger: At startup
4. Action: Start a program
   - Program: `python.exe`
   - Arguments: `run.py --prod`
   - Start in: `ruta\al\proyecto`

### 3.2 Firewall de Windows

```powershell
# Abrir puerto 8050
New-NetFirewallRule -DisplayName "Calculadora Caldera" `
                    -Direction Inbound `
                    -LocalPort 8050 `
                    -Protocol TCP `
                    -Action Allow
```

### 3.3 Configuración de IIS (Opcional)

Para usar IIS como reverse proxy:

1. Instalar ARR (Application Request Routing)
2. Crear regla de rewrite:

```xml
<rule name="ReverseProxyInboundRule1" stopProcessing="true">
    <match url="(.*)" />
    <action type="Rewrite" url="http://localhost:8050/{R:1}" />
</rule>
```

---

## 4. Deployment en Servidor Linux

### 4.1 Instalación en Ubuntu/Debian

```bash
# 1. Actualizar sistema
sudo apt update && sudo apt upgrade -y

# 2. Instalar Python y dependencias
sudo apt install -y python3 python3-pip python3-venv

# 3. Crear usuario para la aplicación
sudo useradd -r -s /bin/false caldera

# 4. Copiar archivos
sudo mkdir -p /opt/caldera
sudo cp -r . /opt/caldera/
sudo chown -R caldera:caldera /opt/caldera

# 5. Crear entorno virtual
cd /opt/caldera
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# 6. Verificar instalación
python -m pytest app/tests/
```

### 4.2 Configurar como Servicio (Systemd)

Crear archivo `/etc/systemd/system/caldera.service`:

```ini
[Unit]
Description=Calculadora de Caldera Acuotubular
After=network.target

[Service]
Type=simple
User=caldera
WorkingDirectory=/opt/caldera
Environment="PATH=/opt/caldera/venv/bin"
ExecStart=/opt/caldera/venv/bin/python run.py --prod
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
```

Activar e iniciar servicio:

```bash
sudo systemctl daemon-reload
sudo systemctl enable caldera
sudo systemctl start caldera
sudo systemctl status caldera
```

### 4.3 Configurar Nginx como Reverse Proxy

Crear archivo `/etc/nginx/sites-available/caldera`:

```nginx
server {
    listen 80;
    server_name caldera.dmlingenieros.com;

    location / {
        proxy_pass http://localhost:8050;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;

        # Para Dash callbacks
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";
    }
}
```

Activar sitio:

```bash
sudo ln -s /etc/nginx/sites-available/caldera /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl reload nginx
```

### 4.4 Configurar HTTPS con Let's Encrypt

```bash
# Instalar certbot
sudo apt install certbot python3-certbot-nginx

# Obtener certificado
sudo certbot --nginx -d caldera.dmlingenieros.com

# Renovación automática (configurada por defecto)
sudo certbot renew --dry-run
```

---

## 5. Deployment con Docker

### 5.1 Crear Dockerfile

```dockerfile
FROM python:3.11-slim

WORKDIR /app

# Instalar dependencias de sistema
RUN apt-get update && apt-get install -y \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Copiar requirements e instalar
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copiar aplicación
COPY . .

# Exponer puerto
EXPOSE 8050

# Usuario no root
RUN useradd -m appuser && chown -R appuser:appuser /app
USER appuser

# Comando de inicio
CMD ["python", "run.py", "--host", "0.0.0.0", "--prod"]
```

### 5.2 Crear docker-compose.yml

```yaml
version: '3.8'

services:
  caldera:
    build: .
    container_name: calculadora-caldera
    ports:
      - "8050:8050"
    restart: unless-stopped
    environment:
      - PYTHONUNBUFFERED=1
    volumes:
      - ./logs:/app/logs
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:8050"]
      interval: 30s
      timeout: 10s
      retries: 3

  # Nginx reverse proxy (opcional)
  nginx:
    image: nginx:alpine
    ports:
      - "80:80"
      - "443:443"
    volumes:
      - ./nginx.conf:/etc/nginx/nginx.conf:ro
      - ./ssl:/etc/nginx/ssl:ro
    depends_on:
      - caldera
```

### 5.3 Comandos Docker

```bash
# Construir imagen
docker build -t calculadora-caldera .

# Ejecutar contenedor
docker run -d -p 8050:8050 --name caldera calculadora-caldera

# Ejecutar con docker-compose
docker-compose up -d

# Ver logs
docker-compose logs -f

# Detener
docker-compose down
```

---

## 6. Configuración de Producción

### 6.1 Variables de Entorno

Crear archivo `.env`:

```bash
# Configuración de servidor
HOST=0.0.0.0
PORT=8050
DEBUG=False

# Logging
LOG_LEVEL=INFO
LOG_FILE=/var/log/caldera/app.log

# Dominio (para URLs en reportes)
DOMAIN=caldera.dmlingenieros.com
```

### 6.2 Modificar run.py para Producción

```python
import os
from dotenv import load_dotenv

load_dotenv()

# Leer configuración desde entorno
args = {
    'host': os.getenv('HOST', '0.0.0.0'),
    'port': int(os.getenv('PORT', 8050)),
    'debug': os.getenv('DEBUG', 'False').lower() == 'true'
}
```

### 6.3 Configuración de Logging

Agregar al archivo de configuración:

```python
import logging

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('/var/log/caldera/app.log'),
        logging.StreamHandler()
    ]
)
```

---

## 7. Monitoreo y Mantenimiento

### 7.1 Monitoreo de Salud

Crear script de health check:

```bash
#!/bin/bash
# health_check.sh

URL="http://localhost:8050"
TIMEOUT=5

if curl -f -s --max-time $TIMEOUT $URL > /dev/null; then
    echo "OK - Aplicación respondiendo"
    exit 0
else
    echo "CRITICAL - Aplicación no responde"
    exit 2
fi
```

### 7.2 Logs Importantes

| Ubicación | Contenido |
|-----------|-----------|
| `/var/log/caldera/app.log` | Logs de la aplicación |
| `/var/log/nginx/` | Logs de Nginx |
`journalctl -u caldera` | Logs de systemd |

### 7.3 Backup

```bash
# Script de backup
#!/bin/bash
DATE=$(date +%Y%m%d_%H%M%S)
BACKUP_DIR="/backup/caldera"
SOURCE_DIR="/opt/caldera"

mkdir -p $BACKUP_DIR
tar -czf $BACKUP_DIR/caldera_$DATE.tar.gz $SOURCE_DIR

# Mantener solo últimos 30 días
find $BACKUP_DIR -name "*.tar.gz" -mtime +30 -delete
```

### 7.4 Actualización

```bash
# 1. Hacer backup
./backup.sh

# 2. Detener servicio
sudo systemctl stop caldera

# 3. Actualizar código
cd /opt/caldera
git pull origin main

# 4. Actualizar dependencias
source venv/bin/activate
pip install -r requirements.txt --upgrade

# 5. Ejecutar tests
python -m pytest app/tests/

# 6. Reiniciar servicio
sudo systemctl start caldera
```

---

## Checklist de Deployment

### Pre-Deployment

- [ ] Código probado en ambiente de desarrollo
- [ ] Tests unitarios pasando (65/65)
- [ ] Dependencias actualizadas
- [ ] Variables de entorno configuradas
- [ ] Backup del sistema actual

### Deployment

- [ ] Código copiado al servidor
- [ ] Dependencias instaladas
- [ ] Servicio configurado (systemd/NSSM)
- [ ] Firewall configurado
- [ ] Reverse proxy configurado (si aplica)
- [ ] SSL/TLS configurado (producción)
- [ ] Logging configurado

### Post-Deployment

- [ ] Servicio iniciado correctamente
- [ ] Aplicación accesible desde navegador
- [ ] Tests funcionales ejecutados
- [ ] Health check configurado
- [ ] Monitoreo configurado
- [ ] Documentación actualizada

---

## Contacto de Soporte

**DML INGENIEROS CONSULTORES S.A.S.**

Para asistencia técnica:
- Email: soporte@dmlingenieros.com
- Tel: +57 XXX XXX XXXX

---

*Documento v1.0 - Febrero 2026*
