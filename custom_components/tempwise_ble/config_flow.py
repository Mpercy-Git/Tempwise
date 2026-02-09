"""Config flow for Tempwise BLE integration."""
import asyncio
import voluptuous as vol
from homeassistant import config_entries
from homeassistant.const import CONF_ADDRESS, CONF_NAME
from homeassistant.data_entry_flow import FlowResult
from bleak import BleakScanner

from .coordinator import TempwiseBLECoordinator

DOMAIN = "tempwise_ble"

# Default UUID for Tempwise BG-BT1W temperature characteristic
DEFAULT_CHAR_UUID = "0000ff01-0000-1000-8000-00805f9b34fb"

CONFIG_SCHEMA = vol.Schema(
    {
        vol.Required(CONF_ADDRESS): str,
        vol.Required("char_uuid", default=DEFAULT_CHAR_UUID): str,
        vol.Required(CONF_NAME, default="Tempwise Thermometer"): str,
    }
)


class TempwiseBLEConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Handle a config flow for Tempwise BLE."""

    VERSION = 1

    async def async_step_user(
        self, user_input: dict | None = None
    ) -> FlowResult:
        """Handle the initial step - offer discovery or manual entry."""
        if user_input is None:
            return self.async_show_menu(
                step_id="user",
                menu_options=["discover", "manual"],
                description_placeholders={},
            )

        # This shouldn't be reached, but handle it
        return await self.async_step_discover()

    async def async_step_discover(
        self, user_input: dict | None = None
    ) -> FlowResult:
        """Discover BLE devices."""
        if user_input is not None:
            # User selected a device from the list
            return await self._async_create_entry_from_device(user_input)

        # Scan for BLE devices
        try:
            devices = await BleakScanner.discover(timeout=10)
            
            # Create a dictionary of devices for selection
            device_list = {}
            for device in devices:
                if device.name:  # Only show devices with names
                    # Display name and MAC address
                    display_name = f"{device.name} ({device.address})"
                    device_list[device.address] = display_name
            
            if not device_list:
                return self.async_abort(reason="no_devices_found")

            return self.async_show_form(
                step_id="discover",
                data_schema=vol.Schema(
                    {
                        vol.Required("device"): vol.In(device_list),
                    }
                ),
                description_placeholders={
                    "device_count": str(len(device_list)),
                },
            )

        except Exception as e:
            return self.async_abort(reason="bluetooth_error")

    async def _async_create_entry_from_device(
        self, user_input: dict
    ) -> FlowResult:
        """Create an entry from discovered device."""
        device_address = user_input["device"]
        device_name = "Tempwise Thermometer"

        try:
            # Validate connection
            coordinator = TempwiseBLECoordinator(
                self.hass,
                device_address,
                DEFAULT_CHAR_UUID,
                device_name,
            )

            return self.async_create_entry(
                title=device_name,
                data={
                    CONF_ADDRESS: device_address,
                    "char_uuid": DEFAULT_CHAR_UUID,
                    CONF_NAME: device_name,
                },
            )

        except Exception as e:
            return self.async_abort(reason="cannot_connect")

    async def async_step_manual(
        self, user_input: dict | None = None
    ) -> FlowResult:
        """Handle manual entry of device address."""
        errors = {}

        if user_input is not None:
            try:
                # Validate the input
                coordinator = TempwiseBLECoordinator(
                    self.hass,
                    user_input[CONF_ADDRESS],
                    user_input.get("char_uuid", DEFAULT_CHAR_UUID),
                    user_input.get(CONF_NAME, "Tempwise Thermometer"),
                )

                # Create entry
                return self.async_create_entry(
                    title=user_input.get(CONF_NAME, "Tempwise Thermometer"),
                    data=user_input,
                )

            except Exception as e:
                errors["base"] = "cannot_connect"

        return self.async_show_form(
            step_id="manual",
            data_schema=vol.Schema(
                {
                    vol.Required(CONF_ADDRESS): str,
                    vol.Required("char_uuid", default=DEFAULT_CHAR_UUID): str,
                    vol.Required(CONF_NAME, default="Tempwise Thermometer"): str,
                }
            ),
            errors=errors,
            description_placeholders={
                "address_hint": "XX:XX:XX:XX:XX:XX",
            },
        )
