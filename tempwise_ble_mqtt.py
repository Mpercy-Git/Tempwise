#!/usr/bin/env python3
"""
Tempwise BG-BT1W BLE to MQTT Bridge with Home Assistant Discovery
Connects to a Bluetooth temperature sensor and publishes readings to MQTT with Home Assistant discovery support.
"""
import asyncio
import time
import json
import logging
import paho.mqtt.client as mqtt
from bleak import BleakClient, BleakScanner, BleakError

# Configuration
ADDRESS = "MAC_ADDRESS"
CHAR_UUID = "xxxxxx"

MQTT_BROKER = "xxxxxx"
MQTT_PORT = 1883
MQTT_TOPIC = "home/sensors/temp"
MQTT_USER = "xxxxxx"
MQTT_PASS = "xxxxxx"

# Home Assistant MQTT Discovery
MQTT_DISCOVERY_PREFIX = "homeassistant"
DEVICE_ID = "tempwise_bg_bt1w"
DEVICE_NAME = "Tempwise Temperature Sensor"
DEVICE_MODEL = "BG-BT1W"

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# MQTT client setup
client_mqtt = mqtt.Client(client_id="tempwise_ble_mqtt", protocol=mqtt.MQTTv311)
client_mqtt.username_pw_set(MQTT_USER, MQTT_PASS)

def publish_discovery():
    """Publish Home Assistant MQTT Discovery message for the temperature sensor."""
    discovery_topic = f"{MQTT_DISCOVERY_PREFIX}/sensor/{DEVICE_ID}/temperature/config"
    
    discovery_payload = {
        "name": f"{DEVICE_NAME} Temperature",
        "unique_id": f"{DEVICE_ID}_temperature",
        "state_topic": MQTT_TOPIC,
        "unit_of_measurement": "°C",
        "device_class": "temperature",
        "icon": "mdi:thermometer",
        "device": {
            "identifiers": [DEVICE_ID],
            "name": DEVICE_NAME,
            "model": DEVICE_MODEL,
            "manufacturer": "Tempwise"
        }
    }
    
    client_mqtt.publish(discovery_topic, json.dumps(discovery_payload), retain=True)
    logger.info("✅ Home Assistant discovery message published")

def on_connect(client, userdata, flags, rc):
    """Called when MQTT broker connection is established."""
    if rc == 0:
        logger.info("✅ Connected to MQTT broker successfully")
        publish_discovery()
    else:
        logger.error(f"❌ MQTT connection error: {rc}")

def on_disconnect(client, userdata, rc):
    """Called when MQTT connection is lost."""
    logger.warning("⚠️ MQTT disconnected, attempting to reconnect...")
    reconnect_mqtt()

def reconnect_mqtt():
    """Reconnect to MQTT broker with retry logic."""
    while True:
        try:
            client_mqtt.connect(MQTT_BROKER, MQTT_PORT, 60)
            logger.info("🔄 MQTT reconnected")
            break
        except Exception as e:
            logger.error(f"❌ Failed to connect to MQTT: {e}, retrying in 5s...")
            time.sleep(5)

client_mqtt.on_connect = on_connect
client_mqtt.on_disconnect = on_disconnect
reconnect_mqtt()
client_mqtt.loop_start()

# BLE notification handler
def handle_notify(sender, data: bytearray):
    """Process BLE temperature data and publish to MQTT."""
    try:
        temp_c = int.from_bytes(data[:2], byteorder="little", signed=True) / 100
        logger.info(f"🌡️ Temperature: {temp_c:.2f} °C")
        client_mqtt.publish(MQTT_TOPIC, f"{temp_c:.2f}")
    except Exception as e:
        logger.error(f"❌ Error decoding data: {e}")

# BLE connection with reconnect logic
async def connect_ble():
    """Connect to BLE device and listen for temperature notifications."""
    while True:
        try:
            logger.info("🔍 Starting BLE scan...")
            device = await BleakScanner.find_device_by_address(ADDRESS, timeout=20)
            
            if not device:
                logger.warning("❌ Device not found, retrying in 10s...")
                await asyncio.sleep(10)
                continue

            async with BleakClient(device, timeout=30.0) as client:
                logger.info("✅ Connected to device!")
                await client.start_notify(CHAR_UUID, handle_notify)
                logger.info("📡 Listening for temperature data (press CTRL+C to stop)...")

                while True:
                    await asyncio.sleep(10)

        except BleakError as e:
            logger.warning(f"⚠️ BLE connection error: {e}, retrying in 5s...")
            await asyncio.sleep(5)
        except Exception as e:
            logger.error(f"❌ Unexpected error: {e}, retrying in 5s...")
            await asyncio.sleep(5)

async def main():
    """Main entry point."""
    logger.info("Starting Tempwise BLE to MQTT bridge...")
    await connect_ble()

if __name__ == "__main__":
    asyncio.run(main())
