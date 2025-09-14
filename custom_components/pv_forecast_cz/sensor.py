"""Sensor platform for PV Forecast."""

from __future__ import annotations

from typing import TYPE_CHECKING

from astral import now
from homeassistant.components.sensor import SensorEntity, SensorEntityDescription

from .entity import PVForecastEntity

if TYPE_CHECKING:
    from homeassistant.core import HomeAssistant
    from homeassistant.helpers.entity_platform import AddEntitiesCallback

    from .coordinator import PVForecastDataUpdateCoordinator
    from .data import PVForecastConfigEntry

ENTITY_DESCRIPTIONS = (
    SensorEntityDescription(
        key="pv_forecast_cz",
        name="PV Forecast Sensor",
        icon="mdi:format-quote-close",
    ),
)


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
        time_str = now().strftime("%Y-%m-%d %H:00:00")
        return self.coordinator.data.get_forecast(time_str)
