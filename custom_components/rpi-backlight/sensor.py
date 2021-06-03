import logging
from datetime import timedelta
from typing import Any, Mapping

# from homeassistant.components.sensor import SensorEntity
from homeassistant.helpers.entity import Entity # , DeviceInfo
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
# from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.update_coordinator import (
    CoordinatorEntity, DataUpdateCoordinator,
)
from homeassistant.helpers import device_registry
from .const import POWER, BRIGHTNESS, CONFIG_ENTRY_ID, DOMAIN
from .device import RaspberryPiDevice

_LOGGER = logging.getLogger(__name__)

SENSOR_TYPES = {
    POWER: {
        "device_value_key": POWER,
        "name": "Screen Power",
        "unit": "",
        "unique_id": "screen_power",
        "icon": "mdi:monitor",
    },
    BRIGHTNESS: {
        "device_value_key": BRIGHTNESS,
        "name": "Screen Brightness",
        "unit": "%",
        "unique_id": "screen_brightness",
        "icon":  "mdi:monitor",
    }
}

async def async_setup_entry(
    hass: HomeAssistant,
    config_entry: ConfigEntry,
    async_add_entities,
) -> None:
    # Get the scan interval for this?
    update_interval = timedelta(seconds=5)
    # entity_id = config_entry.data[CONFIG_ENTRY_ID]
    # TODO: Change CONFIG_ENTRY_ID
    device: RaspberryPiDevice = hass.data[DOMAIN][CONFIG_ENTRY_ID]

    coordinator = DataUpdateCoordinator[Mapping[str, Any]](
        hass,
        _LOGGER,
        name=device.name,
        update_method=device.async_get_data,
        update_interval=update_interval,
    )

    # device.coordinator = coordinator
    await coordinator.async_refresh()

    sensors = [
        PiSensor(coordinator, device, SENSOR_TYPES[BRIGHTNESS]),
        PiSensor(coordinator, device, SENSOR_TYPES[POWER]),
    ]

    async_add_entities(sensors, True)

class PiSensor(CoordinatorEntity, Entity):
    """ Standardizes the sensors """
    def __init__(self,
        coordinator: DataUpdateCoordinator,
        device: RaspberryPiDevice,
        sensor_type: Mapping[str, Any]
    ):
        """ Initialize the brightness sensor """
        super().__init__(coordinator)
        self._device = device
        # Idk how we should do this
        self.sensor_type = sensor_type

    @property
    def available(self) -> bool:
        """Return if entity is available"""
        device_value_key = self.sensor_type["device_value_key"]
        return (
            self.coordinator.last_update_success
            and device_value_key in self.coordinator.data
        )

    @property
    def icon(self) -> str:
        """ Icon to use on the frontend, if any """
        return self.sensor_type["icon"]

    @property
    def name(self) -> str:
        """ Return the name of the sensor """
        return self.sensor_type["name"]

    @property
    def unique_id(self) -> str:
        """ Return an unique ID """
        return self.sensor_type["unique_id"]

    @property
    def unit_of_measurement(self) -> str:
        """Return the unit of measurement of this entity, if any """
        return self.sensor_type["unit"]

    @property
    def device_info(self) -> Mapping[str, Any]:
        """ Get Device Info """
        return {
            "connections": {
                (device_registry.CONNECTION_UPNP, self._device.serial_number)
            },
            "name": self._device.name,
            "manufacturer": self._device.manufacturer,
            "model": self._device.model_name,
        }

    @property
    def state(self) -> str:
        """ Return the state of the device """
        device_value_key = self.sensor_type["device_value_key"]
        return self.coordinator.data[device_value_key]
