"""The Astral Pool Viron eQuilibrium Chlorinator BLE integration."""
from __future__ import annotations

import logging
from pychlorinator.chlorinator import ChlorinatorAPI
from bleak_retry_connector import get_device

from homeassistant.components import bluetooth
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import (
    Platform,
)
from homeassistant.core import Event, HomeAssistant, callback
from homeassistant.const import (
    CONF_ADDRESS,
    CONF_ACCESS_TOKEN,
)
from homeassistant.exceptions import ConfigEntryNotReady

from .coordinator import ChlorinatorDataUpdateCoordinator
from .const import DOMAIN
from .models import ChlorinatorData

PLATFORMS: list[Platform] = [Platform.SENSOR, Platform.BINARY_SENSOR, Platform.SELECT]
_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Set up Chlorinator from a config entry."""

    # coordinator = ChlorinatorDataUpdateCoordinator(hass, chlorinator)

    # hass.data.setdefault(DOMAIN, {})[entry.entry_id] = ChlorinatorData(
    #     entry.title, chlorinator, coordinator
    # )

    # hass.data[DOMAIN][entry.entry_id] = entry.data

    address: str = entry.data[CONF_ADDRESS]
    accesscode: str = entry.data[CONF_ACCESS_TOKEN]
    ble_device = bluetooth.async_ble_device_from_address(
        hass, address.upper(), True
    ) or await get_device(address)
    if not ble_device:
        raise ConfigEntryNotReady(
            f"Could not find chlorinator device with address {address}"
        )

    chlorinator = ChlorinatorAPI(ble_device, accesscode)
    coordinator = ChlorinatorDataUpdateCoordinator(hass, chlorinator)
    await coordinator.async_config_entry_first_refresh()

    hass.data.setdefault(DOMAIN, {})[entry.entry_id] = ChlorinatorData(
        entry.title, chlorinator, coordinator
    )

    hass.async_create_task(
        hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)
    )
    return True


async def _async_update_listener(hass: HomeAssistant, entry: ConfigEntry) -> None:
    """Handle options update."""


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Unload a config entry."""
    await hass.config_entries.async_forward_entry_unload(entry, PLATFORMS)
    return True
