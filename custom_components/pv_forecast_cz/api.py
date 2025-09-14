"""PV Forecast API Client."""

from __future__ import annotations

import socket
from typing import Any

import aiohttp
import async_timeout


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

    URL = "https://www.pvforecast.cz/api/?key={apikey}&lat={latitude:.3f}&lon={longitude:.3f}"

    def __init__(
        self,
        apikey: str,
        session: aiohttp.ClientSession,
    ) -> None:
        """PV Forecast API Client."""
        self._apikey = apikey
        self._session = session

    async def async_get_data(self) -> Any:
        """Get data from the API."""
        lat = 50.055
        lon = 14.222
        return await self._api_wrapper(
            method="get",
            url=PVForecastApiClient.URL.format(
                apikey=self._apikey, latitude=lat, longitude=lon
            ),
        )

    async def async_set_title(self, value: str) -> Any:
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
    ) -> Any:
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
                return await response.text()

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
