"""Sensor platform for Tempwise BLE integration."""
import logging
from homeassistant.components.sensor import (
    SensorEntity,
    SensorDeviceClass,
    SensorStateClass,
)
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import (
    CONF_ADDRESS,
    CONF_NAME,
    UnitOfTemperature,
)
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from .coordinator import TempwiseBLECoordinator

_LOGGER = logging.getLogger(__name__)

DOMAIN = "tempwise_ble"


async def async_setup_entry(
    hass: HomeAssistant,
    config_entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up the sensor platform."""
    device_address = config_entry.data[CONF_ADDRESS]
    char_uuid = config_entry.data["char_uuid"]
    device_name = config_entry.data.get(CONF_NAME, "Tempwise Thermometer")

    # Create coordinator
    coordinator = TempwiseBLECoordinator(
        hass,
        device_address,
        char_uuid,
        device_name,
    )

    # Start connection
    await coordinator.async_start()

    # Store coordinator
    hass.data[DOMAIN][config_entry.entry_id]["coordinator"] = coordinator

    # Create sensor entity
    async_add_entities(
        [TempwiseTemperatureSensor(coordinator, config_entry)],
        True,
    )


class TempwiseTemperatureSensor(SensorEntity):
    """Representation of a Tempwise temperature sensor."""

    _attr_device_class = SensorDeviceClass.TEMPERATURE
    _attr_native_unit_of_measurement = UnitOfTemperature.CELSIUS
    _attr_state_class = SensorStateClass.MEASUREMENT
    _attr_icon = "mdi:thermometer"

    def __init__(self, coordinator: TempwiseBLECoordinator, config_entry: ConfigEntry):
        """Initialize the sensor."""
        self.coordinator = coordinator
        self._config_entry = config_entry
        self._attr_name = f"{coordinator.device_name} Temperature"
        self._attr_unique_id = f"{coordinator.device_address}_temperature".replace(
            ":", "_"
        )

    @property
    def native_value(self) -> float | None:
        """Return the current temperature."""
        return self.coordinator.last_temperature

    @property
    def available(self) -> bool:
        """Return True if entity is available."""
        # Entity is available if we have a temperature reading
        return self.coordinator.last_temperature is not None

    @property
    def device_info(self):
        """Return device information."""
        return {
            "identifiers": {
                (DOMAIN, self.coordinator.device_address),
            },
            "name": self.coordinator.device_name,
            "model": "BG-BT1W",
            "manufacturer": "Tempwise",
        }

    async def async_added_to_hass(self):
        """Register callbacks when entity is added to hass."""
        await super().async_added_to_hass()

        # Register for temperature updates
        self.async_on_remove(
            self.coordinator.register_callback(self._temperature_updated)
        )

    def _temperature_updated(self, temp: float):
        """Callback for temperature updates."""
        self.async_write_ha_state()
