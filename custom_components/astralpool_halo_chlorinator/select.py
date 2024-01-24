"""Platform for select integration."""
from __future__ import annotations

import asyncio
import logging

from pychlorinator import halo_parsers

from homeassistant import config_entries
from homeassistant.components.select import SelectEntity
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity import DeviceInfo
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .const import DOMAIN
from .coordinator import ChlorinatorDataUpdateCoordinator
from .models import ChlorinatorData

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(
    hass: HomeAssistant,
    entry: config_entries.ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up Chlorinator from a config entry."""
    data: ChlorinatorData = hass.data[DOMAIN][entry.entry_id]
    entities = [
        ChlorinatorModeSelect(data.coordinator),
        ChlorinatorSpeedSelect(data.coordinator),
    ]
    async_add_entities(entities)


class ChlorinatorModeSelect(
    CoordinatorEntity[ChlorinatorDataUpdateCoordinator], SelectEntity
):
    """Representation of a Clorinator Select entity."""

    _attr_icon = "mdi:power"
    _attr_options = ["Off", "Auto", "On"]
    _attr_name = "Mode"
    _attr_unique_id = "HCHLOR_mode_select"

    def __init__(
        self,
        coordinator: ChlorinatorDataUpdateCoordinator,
    ) -> None:
        """Initialize the sensor."""
        super().__init__(coordinator)

    @property
    def device_info(self) -> DeviceInfo | None:
        return {
            "identifiers": {(DOMAIN, "HCHLOR")},
            "name": "HCHLOR",
            "model": "Halo Chlor",
            "manufacturer": "Astral Pool",
        }

    @property
    def current_option(self):
        mode = self.coordinator.data.get("mode")
        if mode is halo_parsers.Mode.Off:
            return "Off"
        elif mode is halo_parsers.Mode.Auto:
            return "Auto"
        elif mode is halo_parsers.Mode.On:
            return "On"

    async def async_select_option(self, option: str) -> None:
        """Change the selected option."""
        action: halo_parsers.ChlorinatorActions.NoAction
        if option == "Off":
            action = halo_parsers.ChlorinatorActions.Off
        elif option == "Auto":
            action = halo_parsers.ChlorinatorActions.Auto
        elif option == "On":
            action = halo_parsers.ChlorinatorActions.On
        else:
            action = halo_parsers.ChlorinatorActions.NoAction

        await self.coordinator.chlorinator.async_write_action(action)
        await asyncio.sleep(2)
        await self.coordinator.async_request_refresh()


class ChlorinatorSpeedSelect(
    CoordinatorEntity[ChlorinatorDataUpdateCoordinator], SelectEntity
):
    """Representation of a Clorinator Select entity."""

    _attr_icon = "mdi:pump"
    _attr_options = ["Low", "Medium", "High"]
    _attr_name = "Pump Speed"
    _attr_unique_id = "HCHLOR_speed_select"

    def __init__(
        self,
        coordinator: ChlorinatorDataUpdateCoordinator,
    ) -> None:
        """Initialize the sensor."""
        super().__init__(coordinator)

    @property
    def device_info(self) -> DeviceInfo | None:
        return {
            "identifiers": {(DOMAIN, "HCHLOR")},
            "name": "HCHLOR",
            "model": "Halo Chlor",
            "manufacturer": "Astral Pool",
        }

    @property
    def current_option(self):
        speed = self.coordinator.data.get("pump_speed")
        if speed is halo_parsers.EquipmentParameterCharacteristic.SpeedLevels.Low:
            return "Low"
        elif speed is halo_parsers.EquipmentParameterCharacteristic.SpeedLevels.Medium:
            return "Medium"
        elif speed is halo_parsers.EquipmentParameterCharacteristic.SpeedLevels.High:
            return "High"
        elif speed is halo_parsers.EquipmentParameterCharacteristic.SpeedLevels.AI:
            return "AI"
        # else:
        #     return "High"

    async def async_select_option(self, option: str) -> None:
        """Change the selected option."""
        action: halo_parsers.ChlorinatorActions.NoAction
        if option == "Low":
            action = halo_parsers.ChlorinatorActions.Low
        elif option == "Medium":
            action = halo_parsers.ChlorinatorActions.Medium
        elif option == "High":
            action = halo_parsers.ChlorinatorActions.High
        else:
            action = halo_parsers.ChlorinatorActions.NoAction

        await self.coordinator.chlorinator.async_write_action(action)
        await asyncio.sleep(2)
        await self.coordinator.async_request_refresh()
