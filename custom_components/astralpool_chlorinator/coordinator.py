"""Data coordinator for receiving Chlorinator updates."""

import logging

from datetime import timedelta
from typing import Any

from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity import DeviceInfo
from homeassistant.helpers.update_coordinator import (
    DataUpdateCoordinator,
    UpdateFailed,
)

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
            update_interval=timedelta(seconds=20),
        )
        self._data_age = 0
        self.data = {}
        self.chlorinator = chlorinator
        self.device_info = DeviceInfo(
            identifiers={(DOMAIN, "1234")},
            manufacturer="Astral Pool",
            name="POOL01",
        )

    async def _async_update_data(self):
        """Fetch data from API endpoint."""
        self._data_age += 1
        _LOGGER.debug("_data_age: %s", self._data_age)
        if self._data_age >= 3: # 3 polling events = 60 seconds
            try:
                data = await self.chlorinator.async_gatherdata()
            except Exception:
                _LOGGER.warning("Failed _gatherdata: %s", self._data_age)
                data = {}
            if data != {}:
                self.data = data
                self._data_age = 0
            elif self._data_age >= 15: #15 polling events  = 5 minutes
                self.data = {}
                _LOGGER.error("Failed _gatherdata, giving up: %s", self._data_age)
                raise UpdateFailed("Error communicating with API")
        return self.data
    