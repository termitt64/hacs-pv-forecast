"""PV Forecast API Client."""

from __future__ import annotations

import socket

import aiohttp
import async_timeout

from .forecast_data import ForecastData


class PVForecastApiClientError(Exception):
    """Exception to indicate a general API error."""


class PVForecastApiClientCommunicationError(
    PVForecastApiClientError,
):
    """Exception to indicate a communication error."""


class PVForecastApiClientAuthenticationError(
    PVForecastApiClientError,
):
    """Exception to indicate an authentication error."""


def _verify_response_or_raise(response: aiohttp.ClientResponse) -> None:
    """Verify that the response is valid."""
    if response.status in (401, 403):
        msg = "Invalid credentials"
        raise PVForecastApiClientAuthenticationError(
            msg,
        )
    response.raise_for_status()


class PVForecastApiClient:
    """PV Forecast API Client."""

    """
    key*        Unique client API key
    lat*        Latitude for forecast (3 decimal digits)
    lon*        Longitude for forecast (3 decimal digits)
    forecast    Forecast type (pv - sunshine, temp, rain - rain accumulation)
    format      Data format (simple - plain text, csv, json)
    type        Forecast type (hour, day)
    number      Forecast length (24,48,72 hours, or 1,2,3 days)
    date        Allows to turn on/off timestamp in 'simple' format (1 - on, 0 - off)
    dst         Auto switch to Dayligth Saving Time (1 - on, 0 - off)
    start       Forcast begins (today, tomorrow, auto - 0-12:today 12-24:tomorrow)

    * mandatory parameters
    """
    URL = "https://www.pvforecast.cz/api/?key={apikey}&lat={latitude:.3f}&lon={longitude:.3f}&type=hour&number=72&start=today&format=json&dst=0"

    def __init__(
        self,
        apikey: str,
        session: aiohttp.ClientSession,
    ) -> None:
        """PV Forecast API Client."""
        self._apikey = apikey
        self._session = session

    async def async_get_data(self) -> ForecastData:
        """Get data from the API."""
        lat = 50.055
        lon = 14.222
        return await self._api_wrapper(
            method="get",
            url=PVForecastApiClient.URL.format(
                apikey=self._apikey, latitude=lat, longitude=lon
            ),
        )

    async def async_set_title(self, value: str) -> ForecastData:
        """Get data from the API."""
        return await self._api_wrapper(
            method="patch",
            url="https://jsonplaceholder.typicode.com/posts/1",
            data={"title": value},
            headers={"Content-type": "application/json; charset=UTF-8"},
        )

    async def _api_wrapper(
        self,
        method: str,
        url: str,
        data: dict | None = None,
        headers: dict | None = None,
    ) -> ForecastData:
        """Get information from the API."""
        try:
            async with async_timeout.timeout(10):
                response = await self._session.request(
                    method=method,
                    url=url,
                    headers=headers,
                    json=data,
                )
                _verify_response_or_raise(response)
                return ForecastData(await response.text())

        except TimeoutError as exception:
            msg = f"Timeout error fetching information - {exception}"
            raise PVForecastApiClientCommunicationError(
                msg,
            ) from exception
        except (aiohttp.ClientError, socket.gaierror) as exception:
            msg = f"Error fetching information - {exception}"
            raise PVForecastApiClientCommunicationError(
                msg,
            ) from exception
        except Exception as exception:  # pylint: disable=broad-except
            msg = f"Something really wrong happened! - {exception}"
            raise PVForecastApiClientError(
                msg,
            ) from exception
