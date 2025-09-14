"""Custom types for PV Forecast intregration."""

from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from homeassistant.config_entries import ConfigEntry
    from homeassistant.loader import Integration

    from .api import PVForecastApiClient
    from .coordinator import PVForecastDataUpdateCoordinator


type PVForecastConfigEntry = ConfigEntry[PVForecastData]


@dataclass
class PVForecastData:
    """Data for the PV Forecast integration."""

    client: PVForecastApiClient
    coordinator: PVForecastDataUpdateCoordinator
    integration: Integration
