# PV Forecast

Sun light forecast based on [PV-Forecast][pv-forecast], run by the University Centre for Energy Efficient Buildings, CTU in Prague. Obtaining API key (registration) is needed, to make any use of this integration.

# Installation
You can install the integration using HACS (preferred) or manually.

## HACS (preferred)
1. Open HACS in your Home Assistant instance.
2. Search for "PV Forecast CZ" and install it.
3. Restart Home Assistant.
## Manual
1. Download the custom_components/pv_forecast_cz directory.
2. Copy it into the custom_components folder in your Home Assistant configuration directory.
3. Restart Home Assistant.


# Configuration
In order to get valid forecast from [PV-Forecast](https://wp2.pvforecast.cz/) you have to register (free) to obtain API key for request.
Latitude and Longitute for the forecast is taken automatically from HA configuration.

# Feedback

Feel free to file any bug or feature request directly on [GitHub: termitt64/pv-forecast][issues]

## Buy me a coffee
In case you like this HACS integration, you can support me using LiberaPay

[![liberapay-image]][liberapay-donate]

***
[pv-forecast]: http://pvforecast.cz
[homepage]: https://github.com/termitt64/hacs-pv-forecast
[issues]: https://github.com/termitt64/hacs-pv-forecast/issues
[liberapay-image]: https://liberapay.com/assets/widgets/donate.svg
[liberapay-donate]: https://liberapay.com/termitt64/donate