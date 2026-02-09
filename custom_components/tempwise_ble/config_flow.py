"""Config flow for Tempwise BLE integration."""
import voluptuous as vol
from homeassistant import config_entries
from homeassistant.const import CONF_ADDRESS, CONF_NAME
from homeassistant.data_entry_flow import FlowResult

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
        """Handle the initial step."""
        errors = {}

        if user_input is not None:
            # Validate the input
            try:
                # Test connection
                coordinator = TempwiseBLECoordinator(
                    self.hass,
                    user_input[CONF_ADDRESS],
                    user_input["char_uuid"],
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
            step_id="user",
            data_schema=CONFIG_SCHEMA,
            errors=errors,
            description_placeholders={
                "address_hint": "XX:XX:XX:XX:XX:XX",
                "uuid_hint": "0000xxxx-0000-1000-8000-00805f9b34fb",
            },
        )
