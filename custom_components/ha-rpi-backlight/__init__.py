""" The RaspberryPi Backlight integration. """
import logging
import asyncio
from datetime import timedelta

from homeassistant.config_entries import ConfigEntry
from homeassistant.const import CONF_SCAN_INTERVAL
from homeassistant.core import HomeAssistant, ServiceCall, callback
from homeassistant.helpers.entity_component import EntityComponent
import socketio

from .const import DOMAIN, ATTR_CONFIG

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

    return True

async def async_setup_entry(hass: HomeAssistant, entry):
    """ Setup from config entry """
    config_data = hass.data[DOMAIN].get(ATTR_CONFIG)

    scan_interval = SCANNING_INTERVAL

    if config_data and CONF_SCAN_INTERVAL in config_data:
        scan_interval = config_data.get(CONF_SCAN_INTERVAL) or SCANNING_INTERVAL

    if not "url" in entry.data:
        print("shit went wrong\n")
        return False

    url = entry.data.get("url")

    try:
        # await desktop.connect()
        pass
    except socketio.exceptions.ConnectionError as err:
        _LOGGER.error(err)
        return False

    component = EntityComponent(
        None, DOMAIN, hass, timedelta(seconds=scan_interval)
    )

    # await component.async_add_entities([desktop])

    return True

async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """ Handle removal of entry """
    # TODO: Need to figure out how to a remove an entry

    print(DOMAIN)

    component = EntityComponent(
        None, DOMAIN, hass, timedelta(seconds=SCANNING_INTERVAL)
    )

    for entity in component.entities:
        print(entity)
        await component.async_remove_entity(entity.entity_id)

    return True
