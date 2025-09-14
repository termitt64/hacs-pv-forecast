"""Adds config flow for PVForecast."""

from __future__ import annotations

import voluptuous as vol
from homeassistant import config_entries
from homeassistant.const import CONF_API_KEY, CONF_LATITUDE, CONF_LONGITUDE
from homeassistant.helpers import selector
from homeassistant.helpers.aiohttp_client import async_create_clientsession
from slugify import slugify

from .api import (
    PVForecastApiClient,
    PVForecastApiClientAuthenticationError,
    PVForecastApiClientCommunicationError,
    PVForecastApiClientError,
)
from .const import DOMAIN, LOGGER


class PVForecastFlowHandler(config_entries.ConfigFlow, domain=DOMAIN):
    """Config flow for PVForecast."""

    VERSION = 1

    async def async_step_user(
        self,
        user_input: dict | None = None,
    ) -> config_entries.ConfigFlowResult:
        """Handle a flow initialized by the user."""
        _errors = {}

        hass_latitude = round(self.hass.config.latitude, 3)
        hass_longitude = round(self.hass.config.longitude, 3)

        if user_input is not None:
            try:
                await self._test_key(
                    key=user_input[CONF_API_KEY],
                    lat=user_input[CONF_LATITUDE],
                    lon=user_input[CONF_LONGITUDE],
                )
            except PVForecastApiClientAuthenticationError as exception:
                LOGGER.warning(exception)
                _errors["base"] = "auth"
            except PVForecastApiClientCommunicationError as exception:
                LOGGER.error(exception)
                _errors["base"] = "connection"
            except PVForecastApiClientError as exception:
                LOGGER.exception(exception)
                _errors["base"] = "unknown"
            else:
                await self.async_set_unique_id(
                    ## Do NOT use this in production code
                    ## The unique_id should never be something that can change
                    ## https://developers.home-assistant.io/docs/config_entries_config_flow_handler#unique-ids
                    unique_id=slugify(user_input[CONF_API_KEY])
                )
                self._abort_if_unique_id_configured()
                return self.async_create_entry(
                    title=user_input[CONF_API_KEY],
                    data=user_input,
                )

        return self.async_show_form(
            step_id=None,
            data_schema=vol.Schema(
                {
                    vol.Required(
                        CONF_API_KEY,
                        default=(user_input or {}).get(CONF_API_KEY, vol.UNDEFINED),
                    ): selector.TextSelector(
                        selector.TextSelectorConfig(
                            type=selector.TextSelectorType.TEXT,
                        ),
                    ),
                    vol.Required(
                        CONF_LATITUDE,
                        default=(user_input or {}).get(CONF_LATITUDE, hass_latitude),
                    ): selector.NumberSelector(
                        selector.NumberSelectorConfig(
                            min=48.5,
                            max=51,
                            step=0.001,
                            mode=selector.NumberSelectorMode.BOX,
                        )
                    ),
                    vol.Required(
                        CONF_LONGITUDE,
                        default=(user_input or {}).get(CONF_LONGITUDE, hass_longitude),
                    ): selector.NumberSelector(
                        selector.NumberSelectorConfig(
                            min=12,
                            max=19,
                            step=0.001,
                            mode=selector.NumberSelectorMode.BOX,
                        )
                    ),
                },
            ),
            errors=_errors,
        )

    async def _test_key(self, key: str, lat: float, lon: float) -> None:
        """Validate API key."""
        client = PVForecastApiClient(
            apikey=key,
            session=async_create_clientsession(self.hass),
            latitude=lat,
            longitude=lon,
        )
        await client.async_get_data()
