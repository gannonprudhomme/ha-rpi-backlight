import logging
from datetime import timedelta
from typing import Any, Mapping

from homeassistant.components.sensor import SensorEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.update_coordinator import (
    CoordinatorEntity, DataUpdateCoordinator,
)
from .const import POWER, BRIGHTNESS, CONFIG_ENTRY_ID, DOMAIN
from .device import RaspberryPiDevice

_LOGGER = logging.getLogger(__name__)

SENSOR_TYPES = {
    POWER: {
        "device_value_key": POWER,
        "name": "Screen Power",
        "unit": "something",
        "unique_id": "unique_id",
        "derived_name": "idek",
        "derived_unit": "idek",
        "dervied_unique_id": "idek",
    }
}

async def async_setup_entry(
    hass: HomeAssistant,
    config_entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback
) -> None:
    # Get the scan interval for this?
    update_interval = timedelta(seconds=10)
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
        BrightnessSensor(coordinator, device),
        PowerSensor(coordinator, device)
    ]

    async_add_entities(sensors, True)

# TODO: Standardize these
class BrightnessSensor(CoordinatorEntity, SensorEntity):
    def __init__(self, coordinator: DataUpdateCoordinator, device: RaspberryPiDevice):
        """ Initialize the brightness sensor """
        super().__init__(coordinator)
        self._device = device
        # Idk how we should do this
        self.brightness = 0

    @property
    def available(self) -> bool:
        """Return if entity is available"""
        return True

    @property
    def icon(self) -> str:
        """ Icon to use on the frontend, if any """
        return "mdi:server-network"

    @property
    def available(self) -> bool:
        """ Icon to use on the frontend, if any """
        return True

    @property
    def name(self) -> str:
        """ Return the name of the sensor """
        return "brightness"

    @property
    def unique_id(self) -> str:
        """ Return an unique ID """
        return "brightness"

    @property
    def unit_of_measurement(self) -> str:
        """Return the unit of measurement of this entity, if any """
        return "something"

    @property
    def device_info(self) -> DeviceInfo:
        """ Get Device Info """
        return {
            "connections": "something",
            "name": self._device.name,
            "manufacturer": self._device.manufacturer,
            "model": self._device.model_name,
        }

    @property
    def state(self) -> str | None:
        """ Return the state of the device """
        return str(self.brightness)

class PowerSensor(CoordinatorEntity, SensorEntity):
    def __init__(self, coordinator: DataUpdateCoordinator, device: RaspberryPiDevice):
        """ Initialize the brightness sensor """
        super().__init__(coordinator)
        self._device = device
        # Idk how we should do this
        self.power = False

    @property
    def available(self) -> bool:
        """Return if entity is available"""
        return True

    @property
    def icon(self) -> str:
        """ Icon to use on the frontend, if any """
        return "mdi:server-network"

    @property
    def available(self) -> bool:
        """ Icon to use on the frontend, if any """
        return True

    @property
    def name(self) -> str:
        """ Return the name of the sensor """
        return "screen power"

    @property
    def unique_id(self) -> str:
        """ Return an unique ID """
        return "screen_power"

    @property
    def unit_of_measurement(self) -> str:
        """Return the unit of measurement of this entity, if any """
        return "binary"

    @property
    def device_info(self) -> DeviceInfo:
        """ Get Device Info """
        return {
            "connections": "something",
            "name": "name",
            "manufacturer": None,
            "model": None
        }

    @property
    def state(self) -> str | None:
        """ Return the state of the device """
        return "off"
