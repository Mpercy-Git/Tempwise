#!/bin/bash
# Installation and setup script for Tempwise BLE to MQTT Bridge

set -e

echo "🚀 Installing Tempwise BLE to MQTT Bridge..."

# Check if running as root
if [ "$EUID" -ne 0 ]; then 
   echo "❌ This script must be run as root"
   exit 1
fi

# Install Python dependencies
echo "📦 Installing Python dependencies..."
pip3 install -r requirements.txt

# Copy script to standard location
echo "📋 Installing script..."
mkdir -p /root/tempwise
cp tempwise_ble_mqtt.py /root/tempwise/
cp config_template.py /root/tempwise/config_template.py

# Create configuration file from template if it doesn't exist
if [ ! -f /root/tempwise/config.py ]; then
    echo "⚙️  Creating configuration file..."
    cp /root/tempwise/config_template.py /root/tempwise/config.py
    echo "⚠️  Please edit /root/tempwise/config.py with your settings"
fi

# Create systemd service
echo "🔧 Creating systemd service..."
cat > /etc/systemd/system/tempwise.service << EOF
[Unit]
Description=Tempwise BLE to MQTT Bridge
After=network-online.target
Wants=network-online.target

[Service]
Type=simple
User=root
WorkingDirectory=/root/tempwise
ExecStart=/usr/bin/python3 /root/tempwise/tempwise_ble_mqtt.py
Restart=always
RestartSec=10
StandardOutput=journal
StandardError=journal

[Install]
WantedBy=multi-user.target
EOF

# Enable and start service
echo "▶️  Starting service..."
systemctl daemon-reload
systemctl enable tempwise
systemctl start tempwise

# Check service status
if systemctl is-active --quiet tempwise; then
    echo "✅ Tempwise service started successfully!"
    echo "📋 View logs with: journalctl -u tempwise -f"
else
    echo "❌ Failed to start service. Check logs with: journalctl -u tempwise -n 50"
    exit 1
fi

echo ""
echo "✅ Installation complete!"
echo "📝 Next steps:"
echo "   1. Edit your configuration: nano /root/tempwise/config.py"
echo "   2. Set your Bluetooth MAC address and MQTT credentials"
echo "   3. Check logs: journalctl -u tempwise -f"
echo "   4. Restart service: systemctl restart tempwise"
