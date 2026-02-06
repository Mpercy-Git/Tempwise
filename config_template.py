# Configuration Template for Tempwise BLE to MQTT Bridge

# Device Configuration
# Get Bluetooth MAC address using: bluetoothctl scan on
DEVICE_MAC_ADDRESS = "XX:XX:XX:XX:XX:XX"

# Get characteristic UUID using: gatttool -b [MAC] -I, then: characteristics
CHARACTERISTIC_UUID = "0000xxxx-0000-1000-8000-00805f9b34fb"

# MQTT Broker Configuration
MQTT_BROKER_HOST = "192.168.1.100"  # or "mosquitto.local"
MQTT_BROKER_PORT = 1883
MQTT_USERNAME = "homeassistant"
MQTT_PASSWORD = "your_mqtt_password"

# MQTT Topics
MQTT_TEMPERATURE_TOPIC = "home/sensors/tempwise/temperature"
MQTT_DISCOVERY_PREFIX = "homeassistant"

# Device Information
DEVICE_NAME = "Tempwise Thermometer"
DEVICE_MODEL = "BG-BT1W"
DEVICE_MANUFACTURER = "Tempwise"

# Connection Timeouts
BLE_SCAN_TIMEOUT = 20  # seconds
BLE_CONNECTION_TIMEOUT = 30  # seconds
MQTT_KEEPALIVE = 60  # seconds

# Reconnection Intervals
BLE_RECONNECT_DELAY = 5  # seconds
BLE_DEVICE_NOT_FOUND_DELAY = 10  # seconds
MQTT_RECONNECT_DELAY = 5  # seconds

# Logging
LOG_LEVEL = "INFO"  # DEBUG, INFO, WARNING, ERROR, CRITICAL
