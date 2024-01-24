"""The chlorinator ble integration models."""
from __future__ import annotations

from dataclasses import dataclass

from pychlorinator.halochlorinator import HaloChlorinatorAPI

from .coordinator import ChlorinatorDataUpdateCoordinator


@dataclass
class ChlorinatorData:
    """Data for the chlorinator ble integration."""

    title: str
    device: HaloChlorinatorAPI
    coordinator: ChlorinatorDataUpdateCoordinator
