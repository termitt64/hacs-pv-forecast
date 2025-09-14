"""Adds config flow for PVForecast."""

from __future__ import annotations

import voluptuous as vol
from homeassistant import config_entries
from homeassistant.const import CONF_API_KEY
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

    async def async_step_apikey(
        self,
        user_input: dict | None = None,
    ) -> config_entries.ConfigFlowResult:
        """Handle a flow initialized by the user."""
        _errors = {}
        if user_input is not None:
            try:
                await self._test_key(key=user_input[CONF_API_KEY])
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
            step_id="apikey",
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
                },
            ),
            errors=_errors,
        )

    async def _test_key(self, key: str) -> None:
        """Validate API key."""
        client = PVForecastApiClient(
            apikey=key,
            session=async_create_clientsession(self.hass),
        )
        await client.async_get_data()
