"""The chlorinator ble integration models."""
from __future__ import annotations

from dataclasses import dataclass

from .viron_chlorinator.chlorinator import ChlorinatorAPI
from .coordinator import ChlorinatorDataUpdateCoordinator


@dataclass
class ChlorinatorData:
    """Data for the chlorinator ble integration."""

    title: str
    device: ChlorinatorAPI
    coordinator: ChlorinatorDataUpdateCoordinator
