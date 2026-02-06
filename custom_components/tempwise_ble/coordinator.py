"""BLE Connection Coordinator for Tempwise."""
import asyncio
import logging
from typing import Callable

from bleak import BleakClient, BleakScanner, BleakError
from homeassistant.core import HomeAssistant, callback

_LOGGER = logging.getLogger(__name__)


class TempwiseBLECoordinator:
    """Manages BLE connection to Tempwise device."""

    def __init__(
        self,
        hass: HomeAssistant,
        device_address: str,
        char_uuid: str,
        device_name: str = "Tempwise Thermometer",
    ):
        """Initialize the coordinator."""
        self.hass = hass
        self.device_address = device_address
        self.char_uuid = char_uuid
        self.device_name = device_name
        self._client = None
        self._connected = False
        self._last_temperature = None
        self._callbacks = []
        self._scan_task = None
        self._connect_task = None

    def register_callback(self, callback: Callable[[float], None]) -> Callable:
        """Register a callback for temperature updates."""
        self._callbacks.append(callback)

        def remove_callback():
            self._callbacks.remove(callback)

        return remove_callback

    async def async_connect(self) -> bool:
        """Connect to the BLE device."""
        while not self._connected:
            try:
                _LOGGER.debug("🔍 Starting BLE scan for %s...", self.device_address)
                device = await BleakScanner.find_device_by_address(
                    self.device_address, timeout=20
                )

                if not device:
                    _LOGGER.warning(
                        "❌ Device %s not found, retrying in 10s...",
                        self.device_address,
                    )
                    await asyncio.sleep(10)
                    continue

                _LOGGER.info("✅ Connecting to device: %s", self.device_name)
                self._client = BleakClient(device, timeout=30.0)
                await self._client.connect()
                self._connected = True

                _LOGGER.info(
                    "✅ Connected to %s, starting notifications...", self.device_name
                )
                await self._client.start_notify(
                    self.char_uuid, self._notification_handler
                )

            except BleakError as e:
                _LOGGER.warning(
                    "⚠️ BLE connection error: %s, retrying in 5s...", e
                )
                self._connected = False
                await asyncio.sleep(5)
            except Exception as e:
                _LOGGER.error(
                    "❌ Unexpected error during connection: %s, retrying in 5s...", e
                )
                self._connected = False
                await asyncio.sleep(5)

        return self._connected

    def _notification_handler(self, sender, data: bytearray):
        """Handle BLE notification data."""
        try:
            # Decode temperature from BLE data (2 bytes, little-endian, signed)
            temp_c = int.from_bytes(data[:2], byteorder="little", signed=True) / 100
            self._last_temperature = temp_c
            _LOGGER.debug("🌡️ Temperature: %.2f °C", temp_c)

            # Call registered callbacks
            for callback in self._callbacks:
                callback(temp_c)

        except Exception as e:
            _LOGGER.error("❌ Error decoding temperature data: %s", e)

    async def async_start(self):
        """Start the BLE connection."""
        if not self._connect_task or self._connect_task.done():
            self._connect_task = asyncio.create_task(self.async_connect())

    async def shutdown(self):
        """Shutdown the connection."""
        _LOGGER.info("Shutting down BLE connection...")

        if self._connect_task and not self._connect_task.done():
            self._connect_task.cancel()
            try:
                await self._connect_task
            except asyncio.CancelledError:
                pass

        if self._client and self._connected:
            try:
                await self._client.disconnect()
                self._connected = False
            except Exception as e:
                _LOGGER.error("Error disconnecting: %s", e)

    @property
    def is_connected(self) -> bool:
        """Return connection status."""
        return self._connected

    @property
    def last_temperature(self) -> float | None:
        """Return last temperature reading."""
        return self._last_temperature
