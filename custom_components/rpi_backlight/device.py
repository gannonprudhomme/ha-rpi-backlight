import logging
import socketio
from typing import Mapping, Any

from .const import POWER, BRIGHTNESS, MODEL, SERIAL_NUMBER

_LOGGER = logging.getLogger(__name__)

class RaspberryPiDevice:
    def __init__(self, url: str) -> None:
        """ Initialize """
        self.url = url
        self.sio = socketio.AsyncClient()
        self._data = {}

        self._device_info = {}
        self._serial_number = None
        self._model_name = None

    async def connect(self):
        @self.sio.event
        async def connect():
            _LOGGER.info(f"Connected to {self.url}")

        @self.sio.event
        async def disconnect():
            _LOGGER.info(f"Disconnected from {self.url}")

        _LOGGER.info(f"Attempting to connect to {self.url}")
        try:
            await self.sio.connect(self.url)
            _LOGGER.info("Connected to server at URL %s", self.url)
        except socketio.exceptions.ConnectionError:
            _LOGGER.error("Cannot connect to server at URL %s", self.url)

    @property
    def name(self):
        """ Get the device name """
        return "RaspberryPi"

    @property
    def manufacturer(self) -> str:
        """Get the manufacturer."""
        return "RaspberryPi"

    @property
    def model_name(self) -> str:
        """Get the model name."""
        if self._model_name:
            return self._model_name

        return "Pi"

    @property
    def device_type(self) -> str:
        """Get the device type."""
        return "touchscreen? idk"

    @property
    def serial_number(self) -> str:
        """ Get the serial number """
        if self._serial_number:
            return self._serial_number

        return SERIAL_NUMBER # Temporary

    async def get_device_info(self) -> Mapping[str, str]:
        """ Retrieves model & serial number """
        _LOGGER.debug(f"Getting device info")

        def get_info(data):
            _LOGGER.debug('Received: %s', repr(data))
            if not data:
                self._device_info = {}
                return

            self._serial_number = data.get(SERIAL_NUMBER)
            self._model_name = data.get(MODEL)

        await self.sio.emit("get_device_info", "something", None, get_info)

        return self._device_info

    async def async_get_data(self) -> Mapping[str, Any]:
        """ Get all of the data """
        _LOGGER.debug(f"Getting data from {self.url}")

        async def get_data(data):
            if not data:
                self._data = {}
                return

            _LOGGER.debug(f"Retrieved data {repr(self._data)}")
            self._data = data

        if not self.sio.connected:
            await self.connect()

            if not self.sio.connected:
                return {}

        await self.sio.emit("get_data", "something", None, get_data)

        return self._data

    async def set_brightness(self, brightness: int):
        """ Sets the brightness of the screen """
        if not self.sio.connected:
            _LOGGER.error("set_brightness called but the server is not connected")
            return

        await self.sio.emit("set_brightness", brightness)

    async def set_power(self, power: bool):
        """ Sets the screen power """
        if not self.sio.connected:
            _LOGGER.error("set_power called but the server is not connected")
            return

        await self.sio.emit("set_power", power)

    async def shutdown(self):
        """ Tells the Pi to shutdown """
        if not self.sio.connected:
            _LOGGER.error("shutdown called but the server is not connected")
            return

        await self.sio.emit("shutdown", None)
