"""Config flow for Desktop Processes integration."""
import logging

import voluptuous as vol

from homeassistant import config_entries, core, exceptions

import socketio
from .const import DOMAIN

_LOGGER = logging.getLogger(__name__)

class ConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Handle a config flow for RaspberryPi Backlight."""

    VERSION = 1
    CONNECTION_CLASS = config_entries.CONN_CLASS_LOCAL_POLL

    async def async_step_user(self, user_input=None):
        """Handle the initial step."""
        data_schema = vol.Schema({
            vol.Required("url", default="http://localhost:8080/"): str
        })

        if user_input is None:
            return self.async_show_form(
                step_id="user", data_schema=data_schema
            )

        # Verify that we can connect to this URL? Or nah?
        if "url" not in user_input:
            # raise some error?
            pass

        url = user_input.get("url")

        sio = socketio.AsyncClient()

        try:
            # Connect to make sure it's a valid URL
            # If it isn't, connect will throw a ConnectionError
            await sio.connect(url)
            # Disconnect now that we now it is valid
            await sio.disconnect()
            return self.async_create_entry(title=f"{url}", data={"url": url})
        except socketio.exceptions.ConnectionError as err:
            _LOGGER.exception(err)
            errors = { "base": "did_not_connect" }
            return self.async_show_form(step_id="user", data_schema=data_schema, errors=errors)
        except Exception as e:
            _LOGGER.exception(e)

# Really the only error we need
class CannotConnect(exceptions.HomeAssistantError):
    """Error to indicate we cannot connect."""
