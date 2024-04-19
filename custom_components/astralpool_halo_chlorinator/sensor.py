"""Platform for sensor integration."""

from __future__ import annotations

import logging

from homeassistant import config_entries
from homeassistant.components.sensor import (
    EntityCategory,
    SensorDeviceClass,
    SensorEntity,
    SensorEntityDescription,
    SensorStateClass,
)
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity import DeviceInfo
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .const import DOMAIN
from .coordinator import ChlorinatorDataUpdateCoordinator
from .models import ChlorinatorData

_LOGGER = logging.getLogger(__name__)

CHLORINATOR_SENSOR_TYPES: dict[str, SensorEntityDescription] = {
    "ph_measurement": SensorEntityDescription(
        key="ph_measurement",
        icon="mdi:ph",
        name="pH",
        # native_unit_of_measurement="pH",
        device_class=SensorDeviceClass.PH,
        state_class=SensorStateClass.MEASUREMENT,
    ),
    "mode": SensorEntityDescription(
        key="mode",
        icon="mdi:power",
        name="Mode",
        native_unit_of_measurement=None,
        device_class=SensorDeviceClass.ENUM,
        state_class=None,
    ),
    "pump_speed": SensorEntityDescription(
        key="pump_speed",
        icon="mdi:speedometer",
        name="Pump speed",
        native_unit_of_measurement=None,
        device_class=SensorDeviceClass.ENUM,
        state_class=None,
    ),
    "chlorine_control_status": SensorEntityDescription(
        key="chlorine_control_status",
        icon="mdi:beaker-outline",
        name="Chlorine status",
        native_unit_of_measurement=None,
        device_class=SensorDeviceClass.ENUM,
        state_class=None,
    ),
    "ph_control_status": SensorEntityDescription(
        key="ph_control_status",
        icon="mdi:beaker-outline",
        name="pH status",
        native_unit_of_measurement=None,
        device_class=SensorDeviceClass.ENUM,
        state_class=None,
    ),
    "info_message": SensorEntityDescription(
        key="info_message",
        icon="mdi:information-outline",
        name="Info message",
        native_unit_of_measurement=None,
        device_class=SensorDeviceClass.ENUM,
        state_class=None,
    ),
    "ph_control_setpoint": SensorEntityDescription(
        key="ph_control_setpoint",
        icon="mdi:ph",
        name="pH setpoint",
        # native_unit_of_measurement="pH",
        device_class=SensorDeviceClass.PH,
        state_class=SensorStateClass.MEASUREMENT,
    ),
    "chlorine_control_setpoint": SensorEntityDescription(
        key="chlorine_control_setpoint",
        icon="mdi:beaker-check-outline",
        name="ORP setpoint",
        native_unit_of_measurement=None,
        device_class=None,
        state_class=SensorStateClass.MEASUREMENT,
    ),
    "ORPMeasurement": SensorEntityDescription(
        key="ORPMeasurement",
        icon="mdi:beaker-check-outline",
        name="ORP Measurement",
        native_unit_of_measurement=None,
        device_class=None,
        state_class=SensorStateClass.MEASUREMENT,
    ),
    "ph_control_type": SensorEntityDescription(
        key="ph_control_type",
        icon="mdi:ph",
        name="pH control",
        native_unit_of_measurement=None,
        device_class=SensorDeviceClass.ENUM,
        state_class=None,
    ),
    "chlorine_control_type": SensorEntityDescription(
        key="chlorine_control_type",
        icon="mdi:beaker-outline",
        name="ORP control",
        native_unit_of_measurement=None,
        device_class=SensorDeviceClass.ENUM,
        state_class=None,
    ),
    "PoolLeftFilter": SensorEntityDescription(
        key="PoolLeftFilter",
        icon="mdi:chart-line",
        name="Litres left to Filter",
        native_unit_of_measurement="L",
        device_class=SensorDeviceClass.VOLUME,
        state_class=SensorStateClass.TOTAL,
        entity_category=EntityCategory.DIAGNOSTIC,
    ),
    "DosingPumpSecs": SensorEntityDescription(
        key="DosingPumpSecs",
        icon="mdi:chart-line",
        name="Dosing Pump today (ml)",
        native_unit_of_measurement="mL",
        device_class=SensorDeviceClass.VOLUME,
        state_class=SensorStateClass.TOTAL,
        entity_category=EntityCategory.DIAGNOSTIC,
    ),
    "WaterTemp": SensorEntityDescription(
        key="WaterTemp",
        icon="mdi:temperature-celsius",
        name="Water Temperature",
        native_unit_of_measurement="°C",
        device_class=SensorDeviceClass.TEMPERATURE,
        state_class=SensorStateClass.MEASUREMENT,
    ),
    "CellCurrentmA": SensorEntityDescription(
        key="CellCurrentmA",
        icon="mdi:fuel-cell",
        name="Cell Current",
        native_unit_of_measurement="mA",
        device_class=None,
        state_class=SensorStateClass.MEASUREMENT,
        entity_category=EntityCategory.DIAGNOSTIC,
    ),
    "RealCelllevel": SensorEntityDescription(
        key="RealCelllevel",
        icon="mdi:fuel-cell",
        name="Cell level",
        native_unit_of_measurement=None,
        device_class=None,
        state_class=SensorStateClass.MEASUREMENT,
        entity_category=EntityCategory.DIAGNOSTIC,
    ),
    "PreviousDaysCellLoad": SensorEntityDescription(
        key="PreviousDaysCellLoad",
        icon="mdi:fuel-cell",
        name="Cell Usage Yesterday",
        native_unit_of_measurement="%",
        device_class=None,
        state_class=SensorStateClass.MEASUREMENT,
        entity_category=EntityCategory.DIAGNOSTIC,
    ),
}

HEATER_SENSOR_TYPES: dict[str, SensorEntityDescription] = {
    "HeaterMode": SensorEntityDescription(
        key="HeaterMode",
        icon="mdi:heat-pump",
        name="Heater Mode",
        native_unit_of_measurement=None,
        device_class=SensorDeviceClass.ENUM,
    )
}

SOLAR_SENSOR_TYPES: dict[str, SensorEntityDescription] = {
    "SolarRoof": SensorEntityDescription(
        key="SolarRoof",
        icon="mdi:temperature-celsius",
        name="Solar Roof Temperature",
        native_unit_of_measurement="°C",
        device_class="temperature",
        state_class=SensorStateClass.MEASUREMENT,
    ),
    "SolarWater": SensorEntityDescription(
        key="SolarWater",
        icon="mdi:temperature-celsius",
        name="Solar Water Temperature",
        native_unit_of_measurement="°C",
        device_class="temperature",
        state_class=SensorStateClass.MEASUREMENT,
    ),
    "SolarMode": SensorEntityDescription(
        key="SolarMode",
        icon="mdi:solar-power-variant",
        name="Solar Mode",
        native_unit_of_measurement=None,
        device_class=SensorDeviceClass.ENUM,
        state_class=None,
    ),
}


async def async_setup_entry(
    hass: HomeAssistant,
    entry: config_entries.ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up Chlorinator from a config entry."""
    data: ChlorinatorData = hass.data[DOMAIN][entry.entry_id]
    coordinator = data.coordinator

    async def add_sensor_callback(sensor_type):
        sensor_types_dict = {
            "SolarEnabled": SOLAR_SENSOR_TYPES,
            "HeaterEnabled": HEATER_SENSOR_TYPES,
        }
        sensor_descs = sensor_types_dict.get(sensor_type, {})

        new_entities = []
        for sensor_type, sensor_desc in sensor_descs.items():
            unique_id = f"hchlor_{sensor_type}".lower()
            if unique_id not in coordinator.added_entities:
                new_entities.append(HeaterSensor(coordinator, sensor_desc))
                coordinator.added_entities.add(unique_id)

        if new_entities:
            async_add_entities(new_entities)

    coordinator.add_sensor_callback = add_sensor_callback
    await coordinator.async_config_entry_first_refresh()

    entities = [
        ChlorinatorSensor(data.coordinator, sensor_desc)
        for sensor_desc in CHLORINATOR_SENSOR_TYPES
    ]
    async_add_entities(entities)


class ChlorinatorSensor(
    CoordinatorEntity[ChlorinatorDataUpdateCoordinator], SensorEntity
):
    """Representation of a Clorinator Sensor."""

    _attr_has_entity_name = True
    entity_description: SensorEntityDescription

    def __init__(
        self,
        coordinator: ChlorinatorDataUpdateCoordinator,
        sensor: str,
    ) -> None:
        """Initialize the sensor."""
        super().__init__(coordinator)
        self._sensor = sensor
        self._attr_unique_id = f"HCHLOR_{sensor}".lower()
        self._attr_name = CHLORINATOR_SENSOR_TYPES[sensor].name
        self.entity_description = CHLORINATOR_SENSOR_TYPES[sensor]
        self._attr_native_unit_of_measurement = CHLORINATOR_SENSOR_TYPES[
            sensor
        ].native_unit_of_measurement

    @property
    def device_info(self) -> DeviceInfo | None:
        return {
            "identifiers": {(DOMAIN, "HCHLOR")},
            "name": "HCHLOR",
            "model": "Halo Chlor",
            "manufacturer": "Astral Pool",
        }

    @property
    def native_value(self):
        return self.coordinator.data.get(self._sensor)


class HeaterSensor(CoordinatorEntity[ChlorinatorDataUpdateCoordinator], SensorEntity):
    """Representation of a Heater Sensor."""

    def __init__(self, coordinator, sensor_desc: SensorEntityDescription) -> None:
        """Initialize the sensor."""
        super().__init__(coordinator)
        self._sensor = sensor_desc.key
        self._attr_unique_id = f"hchlor_{self._sensor}".lower()
        self.entity_description = sensor_desc
        self._attr_name = sensor_desc.name
        self._attr_native_unit_of_measurement = sensor_desc.native_unit_of_measurement

    @property
    def device_info(self) -> DeviceInfo | None:
        # Device info remains the same
        return {
            "identifiers": {(DOMAIN, "HCHLOR")},
            "name": "HCHLOR",
            "model": "Halo Chlor",
            "manufacturer": "Astral Pool",
        }

    @property
    def native_value(self):
        # Use self._sensor to fetch the relevant data from coordinator
        return self.coordinator.data.get(self._sensor)
