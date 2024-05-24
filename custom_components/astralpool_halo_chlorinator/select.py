"""Platform for select integration."""

from __future__ import annotations

import asyncio
import logging

from pychlorinator import halo_parsers

from homeassistant import config_entries
from homeassistant.components.select import SelectEntity
from homeassistant.components.switch import SwitchDeviceClass
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
    ]

    async def add_dynamic_select_entities(device_type):
        new_entities = []

        if device_type == "HeaterEnabled" and not hasattr(
            coordinator, "heater_mode_select_added"
        ):
            new_entities.append(HeaterModeSelect(coordinator))
            coordinator.heater_mode_select_added = True  # Prevents re-adding

        if device_type == "SolarEnabled" and not hasattr(
            coordinator, "solar_mode_select_added"
        ):
            new_entities.append(SolarModeSelect(coordinator))
            coordinator.solar_mode_select_added = True  # Prevents re-adding

        if device_type == "LightingEnabled" and not hasattr(
            coordinator, "lighting_mode_select_added"
        ):
            new_entities.append(LightingModeSelect(coordinator))
            coordinator.lighting_mode_select_added = True  # Prevents re-adding

        if new_entities:
            async_add_entities(new_entities)

    # Assign the dynamic entity adder to the coordinator for easy access
    coordinator.add_dynamic_select_entities = add_dynamic_select_entities

    # Initial refresh to ensure current state is up to date
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
        self.coordinator.reset_data_age()
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
        self.coordinator.reset_data_age()
        await asyncio.sleep(1)
        await self.coordinator.async_request_refresh()


class SolarModeSelect(
    CoordinatorEntity[ChlorinatorDataUpdateCoordinator], SelectEntity
):
    """Representation of a Clorinator Select entity."""

    _attr_icon = "mdi:power"
    _attr_options = ["Off", "Auto", "On"]
    _attr_name = "Solar Mode"
    _attr_unique_id = "HCHLOR_solar_onoff_select"

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
        mode = self.coordinator.data.get("SolarMode")

        if mode is halo_parsers.Mode.Off:
            return "Off"
        elif mode is halo_parsers.Mode.Auto:
            return "Auto"
        elif mode is halo_parsers.Mode.On:
            return "On"

    async def async_select_option(self, option: str) -> None:
        """Change the selected option."""
        action: halo_parsers.SolarAppActions.NoAction
        if option == "Off":
            action = halo_parsers.SolarAppActions.Off
        elif option == "Auto":
            action = halo_parsers.SolarAppActions.Auto
        elif option == "On":
            action = halo_parsers.SolarAppActions.On
        else:
            action = halo_parsers.SolarAppActions.NoAction

        _LOGGER.debug("Select Solar entity state changed to %s", action)
        await self.coordinator.chlorinator.async_write_solar_action(action)
        self.coordinator.reset_data_age()
        await asyncio.sleep(1)
        await self.coordinator.async_request_refresh()


class LightingModeSelect(
    CoordinatorEntity[ChlorinatorDataUpdateCoordinator], SelectEntity
):
    """Representation of a Clorinator Light Select entity."""

    _attr_icon = "mdi:power"
    _attr_options = ["Off", "Auto", "On"]
    _attr_name = "Light Mode Zone1"
    _attr_unique_id = "HCHLOR_lightz1_onoff_select"
    _attr_device_class = SwitchDeviceClass.SWITCH

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
        mode = self.coordinator.data.get("LightingMode_1")

        if mode is halo_parsers.Mode.Off:
            return "Off"
        elif mode is halo_parsers.Mode.Auto:
            return "Auto"
        elif mode is halo_parsers.Mode.On:
            return "On"

    async def async_select_option(self, option: str) -> None:
        """Change the selected option."""
        action: halo_parsers.LightAppActions.NoAction
        if option == "Off":
            action = halo_parsers.LightAppActions.TurnOffZone
        elif option == "Auto":
            action = halo_parsers.LightAppActions.SetZoneModeToAuto
        elif option == "On":
            action = halo_parsers.LightAppActions.TurnOnZone
        else:
            action = halo_parsers.LightAppActions.NoAction

        _LOGGER.debug("Select Light Z1 entity state changed to %s", action)
        await self.coordinator.chlorinator.async_write_light_action(action)
        self.coordinator.reset_data_age()
        await asyncio.sleep(1)
        await self.coordinator.async_request_refresh()

    @property
    def is_on(self) -> bool:
        """Return true if the light is on."""
        return self.current_option == "On"

    async def async_turn_on(self, **kwargs):
        """Turn the light on."""
        await self.async_select_option("On")

    async def async_turn_off(self, **kwargs):
        """Turn the light off."""
        await self.async_select_option("Off")
