# Files Removed (MQTT-Only Dependencies)

This project now uses the **native Home Assistant integration** exclusively.

The following MQTT-only files have been removed:
- ~~tempwise_ble_mqtt.py~~ - Standalone MQTT script (no longer needed)
- ~~config_template.py~~ - MQTT configuration template (not applicable)
- ~~install.sh~~ - MQTT systemd installation script (not needed)

## Why?

The native Home Assistant integration (`custom_components/tempwise_ble/`) is:
- ✅ Simpler to set up (UI-based configuration)
- ✅ More reliable (direct Bluetooth, no MQTT broker)
- ✅ Better integrated (proper Home Assistant component)
- ✅ Easier to maintain (no separate service)
- ✅ Professional (HACS compatible)

## If You Need MQTT

If you want the MQTT bridge approach, refer to the git history:
```bash
git log --oneline -- tempwise_ble_mqtt.py
git show <commit>:tempwise_ble_mqtt.py
```

## Current Project Structure

```
custom_components/tempwise_ble/  ← Main integration
├── __init__.py
├── config_flow.py
├── coordinator.py
├── manifest.json
├── sensor.py
└── strings.json

README.md                         ← Documentation
NATIVE_INTEGRATION_GUIDE.md       ← Setup guide
INSTALLATION.md                   ← Quick start
```

No MQTT, no external services, no complex configuration needed! 🎉
