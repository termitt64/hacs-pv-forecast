"""Sensor platform for PV Forecast."""

from __future__ import annotations

import logging
from typing import TYPE_CHECKING

from homeassistant.components.sensor import SensorEntity, SensorEntityDescription
from homeassistant.components.sensor.const import SensorDeviceClass, SensorStateClass
from homeassistant.util import dt as dt_util

from .entity import PVForecastEntity

if TYPE_CHECKING:
    from homeassistant.core import HomeAssistant
    from homeassistant.helpers.entity_platform import AddEntitiesCallback

    from .coordinator import PVForecastDataUpdateCoordinator
    from .data import PVForecastConfigEntry

ENTITY_DESCRIPTIONS = (
    SensorEntityDescription(
        key="photo_energy_forecast_now",
        device_class=SensorDeviceClass.ENERGY,
        state_class=SensorStateClass.MEASUREMENT,
        name="Current photo forecast",
        icon="mdi:solar-power",
    ),
)

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(
    hass: HomeAssistant,  # noqa: ARG001 Unused function argument: `hass`
    entry: PVForecastConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up the sensor platform."""
    async_add_entities(
        PVForecastSensor(
            coordinator=entry.runtime_data.coordinator,
            entity_description=entity_description,
        )
        for entity_description in ENTITY_DESCRIPTIONS
    )


class PVForecastSensor(PVForecastEntity, SensorEntity):
    """PV Forecast Sensor class."""

    def __init__(
        self,
        coordinator: PVForecastDataUpdateCoordinator,
        entity_description: SensorEntityDescription,
    ) -> None:
        """Initialize the sensor class."""
        super().__init__(coordinator)
        self.entity_description = entity_description

    @property
    def native_value(self) -> float | None:
        """Return the native value of the sensor."""
        time_str = dt_util.as_local(dt_util.now()).strftime("%Y-%m-%d %H:00:00")
        _LOGGER.info(f"time: {time_str}")  # noqa: G004
        return self.coordinator.data.get_forecast(time_str)
