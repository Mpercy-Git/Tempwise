# Tempwise BG-BT1W BBQ Thermometer Integration for Home Assistant

![BG-BT1W](https://community-assets.home-assistant.io/optimized/4X/0/c/4/0c4ffbc1a4196d3ebedfa5c810443c94739930b1_2_500x500.jpeg)

This project provides a **native Home Assistant integration** for **Tempwise BG-BT1W** Bluetooth thermometer. The sensor appears directly in Home Assistant with automatic discovery - no additional configuration or external services needed.

---

## ⭐ Key Advantages

- **No MQTT broker needed** - Direct Bluetooth connection to Home Assistant
- **Simple setup** - Configure entirely through Home Assistant UI
- **Reliable** - Automatic reconnection with robust error handling
- **Real-time** - Instant temperature updates via Bluetooth notifications
- **Professional** - Proper Home Assistant component structure
- **HACS ready** - Easy installation and updates via HACS

---

## Installation
Home Assistant 2022.1.0 or newer
- Home Assistant running on system with Bluetooth adapter (Raspberry Pi, NAS, PC, etc.)
- Tempwise BG-BT1W thermometer powered on and in pairing range

### Option 1: Install via HACS (Recommended) ⭐

1. **Open Home Assistant** → Settings → Devices & Services → **HACS** tab
2. Click **"+ Explore & Download Repositories"**
3. Search for **"Tempwise"** 
4. Click the result → **Install**
5. Restart Home Assistant (Settings → System → **Restart**)

### Option 2: Manual Installation

1. Clone the repository:
   ```bash
   cd /config/custom_components
   git clone https://github.com/yourusername/tempwise.git tempwise_ble
   ```

2. Restart Home Assistant:
   - Settings → System → **Restart**

### 3. Add Device in Home Assistant UI

1. **Settings → Devices & Services → Create Automation**
2. Click **"Create Integration"** 
3. Search for **"Tempwise BLE"**
4. Follow the config flow:
   - Enter **Bluetooth MAC address** (format: `XX:XX:XX:XX:XX:XX`)
   - Enter **Characteristic UUID** (format: `0000xxxx-0000-1000-8000-00805f9b34fb`)
   - Enter **Device name** (e.g., "BBQ Thermometer")
5. Click **Finish**

**That's it!** The temperature sensor will appear in Home Assistant automatically.o systemctl enable tempwise
sudo systemctl start tempwise
```

---

## Data Flow

1. **Thermometer** → Bluetooth → **Python/MQTT Script** (publishes data to broker)  
2. **MQTT Broker** → Home Assistant (via MQTT integration)  
3. **Home Assistant** → Creates sensor entity and displays temperature

---

## Home Assistant Integration

### Automatic Configuration (Recommended)

The script automatically publishes Home Assistant MQTT Discovery messages. The sensor will appear automatically in Home Assistant when the script connects successfully.

### Manual Configuration (Optional)

If automatic discovery doesn't work, add this to `configuration.yaml`:

```yaml
mqtt:
  sensor:
    - name: "BG-BT1W Temperature"
      unique_id: "tempwise_bg_bt1w_temperature"
      state_topic: "home/sensors/temp"
      unit_of_measurement: "°C"
      device_class: temperature
      value_template: "{{ value | float(0) }}"
```

---

## Configuration Parameters

| Parameter | Description |
|-----------|-------------|
| `ADDRESS` | Bluetooth MAC address of your BG-BT1W thermometer |
| `CHAR_UUID` | Characteristic UUID containing temperature data |
| `MQTT_BROKER` | IP address or hostname of your MQTT broker |
| `MQTT_PORT` | MQTT port (defaLE → **Home Assistant** (native integration)  
2. **Sensor Entity** → Available in Home Assistant for automation, displays, history, stats
3. **No external services needed** - everything stays local on your Home Assistant system

---

## Using the Sensor in Home Assistant

### View Temperature
- **Dashboard**: Add an "Entities" card with the temperature sensor
- **Settings → Devices & Services**: View the Tempwise device and its entity

### Create Automations

Example: Get notified when temperature is too high

```yaml
alias: BBQ Temperature Alert
trigger:
  platform: numeric_state
  entity_id: sensor.tempwise_thermometer_temperature
  above: 50
action:
  service: notify.notify
  data:
    message: "BBQ temperature is {{ states('sensor.tempwise_thermometer_temperature') }}°C"
```

### Dashboard Card

Add this to your dashboard:
Configured directly in Home Assistant UI. All parameters are set during the config flow:

| Parameter | Description |
|-----------|-------------|
| **Device Address** | Bluetooth MAC address of your BG-BT1W (format: `XX:XX:XX:XX:XX:XX`) |
| **Characteristic UUID** | Temperature characteristic UUID (format: `0000xxxx-0000-1000-8000-00805f9b34fb`) |
| **Device Name** | Friendly name for the device in Home Assistant |

No configuration files needed!
### History & Statistics

The sensor automatically logs temperature history and provides:
- 24-hour history graph
- Weekly/monthly statistics
- Average, min, max temperatures

## Troubleshooting

### Device not found
- Ensure Bluetooth is enabled and the device is powered on
- Check MAC address is correct
- Increase scan timeout in the script

### MQTT connection fails
- Verify broker IP and credentials
- Check firewall allows port 1883
- Ensure MQTT integration is enabled in Home Assistant

### No temperature readings
- Verify characteristic UUID is correct
- Check device is within Bluetooth range
- Review logs for error messages

---

## Releases and Versioning

This project uses automatic versioning:

1. Create a pull request with your changes
2. Add a `release` label and one of: `major`, `minor`, or `patch` label
3. When merged, aprovides:
- **Home Assistant version**: 2022.1.0+
- **Integration type**: Native Custom Integration
- **Device class**: Temperature sensor
- **Entity type**: Sensor with measurement state class
- **Updates**: Real-time BLE notifications
- **Availability**: Tracks connection status
Tag and push to GitHub:
```bash
git tag v1.0.1
git push origin v1.0.1
```

This automatically:
- Creates a GitHub Release
- Publishes to HACS
- Generates release notes from commit messages

---

## Support for Home Assistant

This integration supports:
- **Home Assistant version**: 2022.1.0+
- **Integration type**: MQTT with Discovery
- **Device class**: Temperature sensor
- **Entity type**: Sensor (climate compatible)

---

## License

[Specify your license here]

---

## Credits

- Tempwise BG-BT1W thermometer integration
- Built for Home Assistant Community
device_class – nurodo, kad tai temperatūros sensorius
value_template - sensoriaus reikšmė padauginta iš 100

