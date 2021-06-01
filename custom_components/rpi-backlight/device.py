import logging
import socketio
from typing import Mapping, Any

from .const import POWER, BRIGHTNESS

_LOGGER = logging.getLogger(__name__)

class RaspberryPiDevice:
    def __init__(self, url: str) -> None:
        """ Initialize """
        self.url = url
        self.name = "RaspberryPi"
        self.manufacturer = "pi"
        self.model_name = "3B+"
        self.device_type = "touchscreen? idk"

    # @classmethod
    # async def async_create_device(cls, hass: HomeAssistant) -> RaspberryPiDevice:

    @property
    def name(self):
        """ Get the device name """
        return self.name

    @property
    def manufacturer(self) -> str:
        """Get the manufacturer."""
        return self.manufacturer

    @property
    def model_name(self) -> str:
        """Get the model name."""
        return self.model_name

    @property
    def device_type(self) -> str:
        """Get the device type."""
        return self.device_type

    async def async_get_data(self) -> Mapping[str, Any]:
        """ Get all of the data """
        _LOGGER.debug("Getting data from ")

        return {
            POWER: True,
            BRIGHTNESS: 100
        }
