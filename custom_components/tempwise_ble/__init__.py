"""Tempwise BLE Temperature Sensor Integration."""
import logging
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import Platform
from homeassistant.core import HomeAssistant

_LOGGER = logging.getLogger(__name__)

DOMAIN = "tempwise_ble"
PLATFORMS = [Platform.SENSOR]


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Set up Tempwise BLE from a config entry."""
    hass.data.setdefault(DOMAIN, {})
    
    # Store the entry
    hass.data[DOMAIN][entry.entry_id] = {
        "coordinator": None,
        "device_name": entry.data.get("device_name", "Tempwise Thermometer"),
    }

    # Forward to sensor platform
    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)

    return True


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Unload a config entry."""
    unload_ok = await hass.config_entries.async_unload_platforms(entry, PLATFORMS)

    if unload_ok:
        coordinator = hass.data[DOMAIN][entry.entry_id].get("coordinator")
        if coordinator:
            await coordinator.shutdown()
        hass.data[DOMAIN].pop(entry.entry_id)

    return unload_ok
