"""Platform for binary sensor integration."""
from __future__ import annotations

import logging

from homeassistant import config_entries
from homeassistant.components.binary_sensor import (
    BinarySensorDeviceClass,
    BinarySensorEntity,
    BinarySensorEntityDescription,
)
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity import DeviceInfo
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .const import DOMAIN
from .coordinator import ChlorinatorDataUpdateCoordinator
from .models import ChlorinatorData

_LOGGER = logging.getLogger(__name__)

CHLORINATOR_BINARY_SENSOR_TYPES: dict[str, BinarySensorEntityDescription] = {
    "pump_is_operating": BinarySensorEntityDescription(
        key="pump_is_operating",
        device_class=BinarySensorDeviceClass.RUNNING,
        icon="mdi:pump",
        name="Pump",
    ),
    # "pump_is_priming": BinarySensorEntityDescription(
    #     key="pump_is_priming",
    #     device_class=BinarySensorDeviceClass.RUNNING,
    #     icon="mdi:reload",
    #     name="Pump priming",
    # ),
    # "chemistry_values_current": BinarySensorEntityDescription(
    #     key="chemistry_values_current",
    #     icon="mdi:check-circle-outline",
    #     name="Chemistry values current",
    # ),
    # "chemistry_values_valid": BinarySensorEntityDescription(
    #     key="chemistry_values_valid",
    #     icon="mdi:check-circle",
    #     name="Chemistry values valid",
    # ),
    "cell_is_operating": BinarySensorEntityDescription(
        key="cell_is_operating",
        device_class=BinarySensorDeviceClass.RUNNING,
        icon="mdi:fuel-cell",
        name="Cell",
    ),
    # "sanitising_until_next_timer_tomorrow": BinarySensorEntityDescription(
    #     key="sanitising_until_next_timer_tomorrow",
    #     icon="mdi:fuel-cell",
    #     name="Sanitising until next timer tomorrow",
    # ),
}


async def async_setup_entry(
    hass: HomeAssistant,
    entry: config_entries.ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up Chlorinator binary sensors from a config entry."""
    data: ChlorinatorData = hass.data[DOMAIN][entry.entry_id]

    entities = [
        ChlorinatorBinarySensor(data.coordinator, sensor_desc)
        for sensor_desc in CHLORINATOR_BINARY_SENSOR_TYPES
    ]
    async_add_entities(entities)


class ChlorinatorBinarySensor(CoordinatorEntity, BinarySensorEntity):
    """Representation of a Clorinator binary sensor."""

    _attr_name = "Pump is operating"

    def __init__(
        self,
        coordinator: ChlorinatorDataUpdateCoordinator,
        sensor: str,
    ) -> None:
        """Initialize the sensor."""
        super().__init__(coordinator)
        self._sensor = sensor
        self._attr_unique_id = f"HCHLOR_{sensor}".lower()
        self._attr_name = CHLORINATOR_BINARY_SENSOR_TYPES[sensor].name
        self.entity_description = CHLORINATOR_BINARY_SENSOR_TYPES[sensor]
        self._attr_device_class = CHLORINATOR_BINARY_SENSOR_TYPES[sensor].device_class

    @property
    def device_info(self) -> DeviceInfo | None:
        return {
            "identifiers": {(DOMAIN, "HCHLOR")},
            "name": "HCHLOR",
            "model": "Viron eQuilibrium",
            "manufacturer": "Astral Pool",
        }

    @property
    def is_on(self) -> bool:
        """Return the state of the sensor."""
        return self.coordinator.data.get(self._sensor)
