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

HEATER_BINARY_SENSOR_TYPES: dict[str, BinarySensorEntityDescription] = {
    "HeaterOn": BinarySensorEntityDescription(
        key="HeaterOn",
        device_class=BinarySensorDeviceClass.RUNNING,
        icon="mdi:fire",
        name="Heater On",
    )
}

SOLAR_BINARY_SENSOR_TYPES: dict[str, BinarySensorEntityDescription] = {
    "SolarPumpState": BinarySensorEntityDescription(
        key="SolarPumpState",
        device_class=BinarySensorDeviceClass.RUNNING,
        icon="mdi:pump",
        name="Solar Pump On",
    )
}


async def async_setup_entry(
    hass: HomeAssistant,
    entry: config_entries.ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up Chlorinator binary sensors from a config entry."""
    data: ChlorinatorData = hass.data[DOMAIN][entry.entry_id]
    coordinator = data.coordinator

    async def add_binary_sensor_callback(sensor_type):
        binary_sensor_types_dict = {
            "SolarEnabled": SOLAR_BINARY_SENSOR_TYPES,
            "HeaterEnabled": HEATER_BINARY_SENSOR_TYPES,
        }
        sensor_descs = binary_sensor_types_dict.get(sensor_type, {})

        new_entities = []
        for sensor_type, sensor_desc in sensor_descs.items():
            unique_id = f"hchlor_{sensor_type}".lower()
            if unique_id not in coordinator.added_entities:
                new_entities.append(HeaterBinarySensor(coordinator, sensor_desc))
                coordinator.added_entities.add(unique_id)

        if new_entities:
            async_add_entities(new_entities)

    coordinator.add_binary_sensor_callback = add_binary_sensor_callback
    await coordinator.async_config_entry_first_refresh()

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
            "model": "Halo Chlor",
            "manufacturer": "Astral Pool",
        }

    @property
    def is_on(self) -> bool:
        """Return the state of the sensor."""
        return self.coordinator.data.get(self._sensor)


class HeaterBinarySensor(CoordinatorEntity, BinarySensorEntity):
    """Representation of a Clorinator binary sensor."""

    _attr_name = "Pump is operating"

    def __init__(self, coordinator, sensor_desc: BinarySensorEntityDescription):
        """Initialize the sensor."""
        super().__init__(coordinator)
        self._sensor = sensor_desc.key
        self._attr_unique_id = f"hchlor_{self._sensor}".lower()
        self.entity_description = sensor_desc
        self._attr_name = sensor_desc.name
        self._attr_device_class = sensor_desc.device_class

    @property
    def device_info(self) -> DeviceInfo | None:
        return {
            "identifiers": {(DOMAIN, "HCHLOR")},
            "name": "HCHLOR",
            "model": "Halo Chlor",
            "manufacturer": "Astral Pool",
        }

    @property
    def is_on(self) -> bool:
        """Return the state of the sensor."""
        return self.coordinator.data.get(self._sensor)
