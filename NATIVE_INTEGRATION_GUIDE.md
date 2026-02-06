# Native Home Assistant Bluetooth Integration Guide

## Overview

This is a **native Home Assistant custom integration** - it connects directly to the Tempwise BG-BT1W via Bluetooth **without requiring MQTT or any external services**.

### How It Works

```
Tempwise Thermometer
         ↓ (Bluetooth LE)
Home Assistant Instance
         ↓
Sensor Entity (Real-time updates)
         ↓
Automations, Dashboards, History
```

## Installation Steps

### Step 1: Install the Integration

**Via HACS (Easiest):**
1. Home Assistant → Settings → Devices & Services → HACS tab
2. Click "+ Explore & Download Repositories"
3. Search for "Tempwise"
4. Click Install
5. Restart Home Assistant

**Via Manual Installation:**
1. Download the `custom_components/tempwise_ble` folder
2. Copy to `/config/custom_components/tempwise_ble`
3. Restart Home Assistant

### Step 2: Add Device to Home Assistant

1. Go to **Settings → Devices & Services → Integrations**
2. Click **"Create Integration"** (bottom right)
3. Search for **"Tempwise BLE"**
4. Fill in the form:
   - **Device Bluetooth Address**: `XX:XX:XX:XX:XX:XX` (see below how to find)
   - **Characteristic UUID**: `0000xxxx-0000-...` (see below how to find)
   - **Device Name**: "BBQ Thermometer" or whatever you prefer
5. Click **Finish**

**The integration is now active!** The sensor will appear in Home Assistant.

---

## Finding Device Information

### Find Bluetooth MAC Address

**On Linux/Raspberry Pi:**
```bash
bluetoothctl scan on
```

Look for your Tempwise device in the output. It will show something like:
```
[NEW] Device XX:XX:XX:XX:XX:XX Tempwise
[NEW] Device XX:XX:XX:XX:XX:XX BG-BT1W
```

**On Windows 10+:**
1. Settings → Devices → Bluetooth & Other Devices
2. Look for your Tempwise device
3. Click it → Properties → MAC address shown

### Find Characteristic UUID

**On Linux with gatttool:**
```bash
# Start interactive mode
gatttool -b XX:XX:XX:XX:XX:XX -I

# List all characteristics
[XX:XX:XX:XX:XX:XX][LE]> characteristics

# Look for one that contains temperature data
# Usually a UUID like: 0000xxxx-0000-1000-8000-00805f9b34fb
```

**On Home Assistant:**
If you know the MAC address, try common UUIDs first:
- `0000180a-0000-1000-8000-00805f9b34fb` (Device Information)
- `00002a19-0000-1000-8000-00805f9b34fb` (Battery Level)
- Check device manual or reverse engineer

---

## Using the Integration

### Entity Name

The sensor will be named like: `sensor.tempwise_thermometer_temperature`

You can find it in:
- **Settings → Devices & Services → Entities** (search for "tempwise")
- **Settings → Automations & Scenes → Devices** (under Tempwise device)

### Add to Dashboard

**Using the UI (Easiest):**
1. Go to your Dashboard
2. Click the three dots → Edit Dashboard
3. Click "Create New Card"
4. Choose "Entity" card type
5. Select `sensor.tempwise_thermometer_temperature`
6. Click Save

**Using YAML:**
```yaml
type: entities
title: BBQ Temperature
entities:
  - entity: sensor.tempwise_thermometer_temperature
    icon: mdi:thermometer
    format: precision2
```

### Create Automations

**Example 1: Alert when temperature is high**
```yaml
alias: BBQ Alert - High Temperature
description: ""
trigger:
  - platform: numeric_state
    entity_id:
      - sensor.tempwise_thermometer_temperature
    above: "50"
condition: []
action:
  - service: notify.mobile_app_phone
    data:
      message: "BBQ temperature is {{ states('sensor.tempwise_thermometer_temperature') }}°C!"
      title: "⚠️ High Temperature"
mode: single
```

**Example 2: Log temperature every 5 minutes**
```yaml
alias: Log BBQ Temperature
description: ""
trigger:
  - platform: time_pattern
    minutes: "5"
action:
  - service: logger.log
    data:
      level: INFO
      message: "BBQ Temp: {{ states('sensor.tempwise_thermometer_temperature') }}°C"
mode: single
```

**Example 3: Send notification when cooking starts (above 30°C)**
```yaml
alias: Cooking Started
trigger:
  - platform: numeric_state
    entity_id:
      - sensor.tempwise_thermometer_temperature
    above: "30"
action:
  - service: notify.notify
    data:
      message: "BBQ cooking started!"
mode: single
```

### View History

1. Click on the sensor entity → History tab
2. View 24-hour temperature graph
3. See min/max/average statistics

---

## Troubleshooting

### Integration Won't Add

**Error: "Failed to connect"**
- Check Bluetooth MAC address is correct (format: `XX:XX:XX:XX:XX:XX`)
- Ensure device is powered on and in range
- Try increasing BLE scan timeout in code

**Error: "Invalid characteristic UUID"**
- Verify characteristic UUID format: `0000xxxx-0000-1000-8000-00805f9b34fb`
- Check it's the temperature characteristic (not battery, etc.)
- Try common UUIDs from device manual

### Sensor Not Updating

**Not receiving temperature readings:**
1. Check Home Assistant logs: Settings → System → Logs → Look for "tempwise" errors
2. Ensure Bluetooth adapter is working on Home Assistant device
3. Verify device is in range and powered on
4. Try removing and re-adding the integration

**Connection keeps dropping:**
1. Check device is within Bluetooth range
2. Try moving closer to Home Assistant device
3. Restart the integration: Settings → Devices & Services → Three dots on Tempwise device → Restart

### Check Logs

View detailed logs to diagnose issues:
```
Settings → System → Logs
Search for "tempwise" entries
```

---

## Advanced Configuration

### Adjust in Code (Optional)

Edit `custom_components/tempwise_ble/coordinator.py`:

```python
# BLE Scan Timeout (seconds)
timeout=20

# Connection Timeout (seconds)
timeout=30.0

# Reconnect delay (seconds)
await asyncio.sleep(5)
```

### Disable Integration Temporarily

1. Settings → Devices & Services
2. Find Tempwise device
3. Click three dots → Disable

---

## Uninstalling

1. **Settings → Devices & Services → Integrations**
2. Find **Tempwise BLE**
3. Click three dots → Delete
4. Delete the folder: `custom_components/tempwise_ble`
5. Restart Home Assistant

---

## What Makes This Better Than MQTT?

| Feature | Native HA | MQTT |
|---------|-----------|------|
| **Extra services needed** | None | MQTT broker required |
| **Complexity** | Simple UI setup | Requires manual config |
| **Dependencies** | Just Bleak | MQTT + Paho |
| **Configuration** | UI based | File based |
| **Reliability** | Direct connection | Network dependent |
| **Setup time** | 2 minutes | 15+ minutes |

---

## Support

For issues:
1. Check logs: Settings → System → Logs
2. Search GitHub issues
3. Create a new issue with:
   - Home Assistant version
   - Error logs (truncate your MAC address for privacy)
   - Device model and Bluetooth address (hidden)

---

**Enjoy your native Tempwise integration! 🎉**
