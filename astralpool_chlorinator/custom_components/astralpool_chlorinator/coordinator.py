"""Data coordinator for receiving Chlorinator updates."""

import logging

from datetime import timedelta
from typing import Any

from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity import DeviceInfo
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator

from pychlorinator.chlorinator import ChlorinatorAPI
from .const import DOMAIN

_LOGGER = logging.getLogger(__name__)


class ChlorinatorDataUpdateCoordinator(DataUpdateCoordinator[dict[str, Any]]):
    """Data coordinator for getting Chlorinator updates."""

    def __init__(self, hass: HomeAssistant, chlorinator: ChlorinatorAPI) -> None:
        """Initialise the coordinator."""
        super().__init__(
            hass,
            _LOGGER,
            name=DOMAIN,
            update_interval=timedelta(minutes=1),
        )
        self.data = {}
        self.chlorinator = chlorinator
        self.device_info = DeviceInfo(
            identifiers={(DOMAIN, "1234")},
            manufacturer="Astral Pool",
            name="POOL01",
        )

    async def _async_update_data(self):
        """Fetch data from API endpoint."""
        data = await self.chlorinator.async_gatherdata()
        return data
