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
    coordinator = data.coordinator
    entities = [
        ChlorinatorModeSelect(data.coordinator),
        # HeaterModeSelect(data.coordinator),
        # ChlorinatorSpeedSelect(data.coordinator),
    ]

    async def add_heater_select_callback():  # Callback renamed and no parameters
        unique_id = (
            "hchlor_heater_mode_select"  # Example unique ID for HeaterModeSelect
        )
        if unique_id not in coordinator.added_entities:
            async_add_entities([HeaterModeSelect(coordinator)], update_before_add=True)
            coordinator.added_entities.add(unique_id)  # Mark as added

    coordinator.add_heater_select_callback = add_heater_select_callback
    await coordinator.async_config_entry_first_refresh()

    async_add_entities(entities)


class ChlorinatorModeSelect(
    CoordinatorEntity[ChlorinatorDataUpdateCoordinator], SelectEntity
):
    """Representation of a Clorinator Select entity."""

    _attr_icon = "mdi:power"
    _attr_options = ["Off", "Auto", "Low", "Medium", "High"]
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
        speed = self.coordinator.data.get("pump_speed")

        if mode is halo_parsers.Mode.Off:
            return "Off"
        elif mode is halo_parsers.Mode.Auto:
            return "Auto"
        elif mode is halo_parsers.Mode.On:
            if speed is halo_parsers.EquipmentParameterCharacteristic.SpeedLevels.Low:
                return "Low"
            elif (
                speed
                is halo_parsers.EquipmentParameterCharacteristic.SpeedLevels.Medium
            ):
                return "Medium"
            elif (
                speed is halo_parsers.EquipmentParameterCharacteristic.SpeedLevels.High
            ):
                return "High"

    async def async_select_option(self, option: str) -> None:
        """Change the selected option."""
        action: halo_parsers.ChlorinatorActions.NoAction
        if option == "Off":
            action = halo_parsers.ChlorinatorActions.Off
        elif option == "Auto":
            action = halo_parsers.ChlorinatorActions.Auto
        elif option == "Low":
            action = halo_parsers.ChlorinatorActions.Low
        elif option == "Medium":
            action = halo_parsers.ChlorinatorActions.Medium
        elif option == "High":
            action = halo_parsers.ChlorinatorActions.High
        else:
            action = halo_parsers.ChlorinatorActions.NoAction

        _LOGGER.debug("Select entity state changed to %s", action)
        await self.coordinator.chlorinator.async_write_action(action)
        await asyncio.sleep(1)
        await self.coordinator.async_request_refresh()


class HeaterModeSelect(
    CoordinatorEntity[ChlorinatorDataUpdateCoordinator], SelectEntity
):
    """Representation of a Clorinator Select entity."""

    _attr_icon = "mdi:power"
    _attr_options = ["Off", "On"]
    _attr_name = "Heater Mode"
    _attr_unique_id = "HCHLOR_heater_onoff_select"

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
        mode = self.coordinator.data.get("HeaterMode")

        if mode is halo_parsers.HeaterStateCharacteristic.HeaterModeValues.Off:
            return "Off"
        # elif mode is halo_parsers.HeaterStateCharacteristic.HeaterModeValues.Auto:
        #     return "Auto"
        elif mode is halo_parsers.HeaterStateCharacteristic.HeaterModeValues.On:
            return "On"

    async def async_select_option(self, option: str) -> None:
        """Change the selected option."""
        action: halo_parsers.HeaterAppActions.NoAction
        if option == "Off":
            action = halo_parsers.HeaterAppActions.HeaterOff
        # elif option == "Auto":
        #     action = halo_parsers.HeaterAppActions.Auto
        elif option == "On":
            action = halo_parsers.HeaterAppActions.HeaterOn
        else:
            action = halo_parsers.HeaterAppActions.NoAction

        _LOGGER.debug("Select Heater entity state changed to %s", action)
        await self.coordinator.chlorinator.async_write_heater_action(action)
        await asyncio.sleep(1)
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

        _LOGGER.debug("Select entity state changed to %s", action)

        # await self.coordinator.chlorinator.async_write_action(action)
        await asyncio.sleep(2)
        await self.coordinator.async_request_refresh()
