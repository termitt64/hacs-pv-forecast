"""Data classes for PV Forecast integration."""

import json


class ForecastData:
    """Data class for PV Forecast integration."""

    def __init__(self, data: str) -> None:
        """Initialize instance with list of pairs."""
        self._data = dict(json.loads(data))

    def get_forecast(self, time: str) -> float:
        """Return forecast for given datetime (YYYY-MM-dd HH:mm:ss)."""
        return self._data[time]
