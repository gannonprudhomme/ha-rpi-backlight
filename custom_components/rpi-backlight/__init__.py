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
from .const import DOMAIN, ATTR_CONFIG, CONFIG_ENTRY_ID

_LOGGER = logging.getLogger(__name__)

SCANNING_INTERVAL = 5


@callback
async def _set_brightness(call: ServiceCall):
    """ Handle the call """

@callback
async def _set_screen_power(call: ServiceCall):
    """ Handle the call """

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

    hass.data[DOMAIN][CONFIG_ENTRY_ID] = device

    dev_reg = await device_registry.async_get_registry(hass)
    dev_reg.async_get_or_create(
        config_entry_id=entry.entry_id,
        connections={(device_registry.CONNECTION_NETWORK_MAC, "abcde")},
        identifiers={(DOMAIN, "abcde")},
        name=device.name,
        manufacturer=device.manufacturer,
        model=device.model_name,
    )

    hass.config_entries.async_setup_platforms(entry, ["sensor"])

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
