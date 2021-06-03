""" The RaspberryPi Backlight integration. """
import logging
import asyncio
from datetime import timedelta

from homeassistant.config_entries import ConfigEntry
from homeassistant.const import CONF_SCAN_INTERVAL
from homeassistant.core import HomeAssistant, ServiceCall, callback
from homeassistant.helpers.entity_component import EntityComponent
from homeassistant.helpers import device_registry
import socketio

from .device import RaspberryPiDevice
from .const import DOMAIN, ATTR_CONFIG, CONFIG_ENTRY_ID, MODEL, SERIAL_NUMBER

_LOGGER = logging.getLogger(__name__)

SCANNING_INTERVAL = 30

# TODO: Add entity_id specifiying so we can have multiple Pi's
devices = []

@callback
async def _set_brightness(call: ServiceCall):
    """ Handle the call """
    brightness = call.data.get("brightness")

    if brightness is None:
        _LOGGER.error("brightness must be passed to set_brightness")
        return

    if len(devices) == 0:
        _LOGGER.error("Attempting to set brightness with no available devices")
        return
    
    # Assuming only one device at the momement
    device = devices[0]
    await device.set_brightness(brightness)

@callback
async def _set_screen_power(call: ServiceCall):
    """ Handle the call """
    power = call.data.get("power")

    if power is None:
        _LOGGER.error("power must be passed to set_power")
        return

    if len(devices) == 0:
        _LOGGER.error("Attempting to set brightness with no available devices")
        return

    device = devices[0]
    await device.set_power(power)

@asyncio.coroutine
async def async_setup(hass: HomeAssistant, config: dict):
    """ Set up the Desktop Processes component. """
    # Setup data so we can pass the config data to async_setup_entry
    hass.data.setdefault(DOMAIN, {})
    hass.data[DOMAIN] = {}
    hass.data[DOMAIN][ATTR_CONFIG] = config.get(DOMAIN)

    hass.services.async_register(DOMAIN, "set_brightness", _set_brightness)
    hass.services.async_register(DOMAIN, "set_screen_power", _set_screen_power)

    return True

async def async_setup_entry(hass: HomeAssistant, entry):
    """ Setup from config entry """
    config_data = hass.data[DOMAIN].get(ATTR_CONFIG)

    scan_interval = SCANNING_INTERVAL

    if config_data and CONF_SCAN_INTERVAL in config_data:
        scan_interval = config_data.get(CONF_SCAN_INTERVAL) or SCANNING_INTERVAL

    url = entry.data.get("url")

    # Create the device
    device = RaspberryPiDevice(url)
    await device.connect()

    # info = await device.get_device_info()

    devices.append(device)

    serial_number = SERIAL_NUMBER

    # TODO: Make this not use CONFIG_ENTRY_ID
    hass.data[DOMAIN][CONFIG_ENTRY_ID] = device

    dev_reg = await device_registry.async_get_registry(hass)
    dev_reg.async_get_or_create(
        config_entry_id=entry.entry_id,
        connections={(device_registry.CONNECTION_UPNP, device.serial_number)},
        identifiers={(DOMAIN, device.serial_number)},
        name=device.name,
        manufacturer=device.manufacturer,
        model=device.model_name,
    )

    hass.async_create_task(hass.config_entries.async_forward_entry_setup(entry, "sensor"))

    return True

async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """ Handle removal of entry """
    # Get the according component so we can get the entities it contains
    """
    component = hass.data[DOMAIN]["component"]

    # Must convert it to a list, otherwise we'll get a "dict size changed during iteration"
    entities = list(component.entities)

    # There will only be one, but iterate anyways
    for entity in entities:
        await component.async_remove_entity(entity.entity_id)
    """

    return True
