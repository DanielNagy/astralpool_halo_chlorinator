# Astral Pool Halo Chlorinator

### No Affiliation with Astral Pools or Fluidra

[![GitHub Release][releases-shield]][releases]
[![GitHub Activity][commits-shield]][commits]
[![License][license-shield]](LICENSE)

[![pre-commit][pre-commit-shield]][pre-commit]
[![Black][black-shield]][black]

[![hacs][hacsbadge]][hacs]
[![Project Maintenance][maintenance-shield]][user_profile]

[![Community Forum][forum-shield]][forum]

[![BuyMeCoffee][buymecoffeebadge]][buymecoffee]

Please also support https://github.com/pbutterworth/astralpool_chlorinator for his initial work with the Astral Viron EQ Chlorinator.

\*\*This component will set up the following platforms.\*\*

| Platform        | Description                                      |
| --------------- | ------------------------------------------------ |
| `binary_sensor` | Show something `True` or `False`.                |
| `sensor`        | Show info from Astral Pool Halo Chlorinator API. |
| `select`        | Control the chlorinator mode (off/auto/manual)   |

# Pre-Requisites

### Astral Halo Minimum Firmware Version 2.2

## Hardware

1. Obtain an ESP32 dev board. The [M5Stack Atom Lite](https://shop.m5stack.com/products/atom-lite-esp32-development-kit?ref=NabuCasa) is a great choice for first timers. If you are handy with a soldering iron, and you want a professional PoE powered BLE Proxy. Obtain a GL.iNet GL-S10, and follow the Instructions at [blakadder.com](https://blakadder.com/gl-s10) on how to converting it to a ESPHome Bluetooth Proxy. _The GL-S10 has a external antenna which will provide better range than a typical esp32 dev board_
2. Connect your ESP32 to your computer with a USB Data Cable. Double-check it actually _IS_ actually a data cable and not just a charge cable.

## Install a Bluetooth Proxy to the ESP board

3. Visit https://esphome.io/projects/?type=bluetooth.
4. Select "Bluetooth Proxy" and your device type.
5. Flash your device.
6. Join it to your WiFi network.
7. Add it to Home Assistant as an ESPHome device. You _do not_ need the ESPHome server running, just the ESPHome device discovered.
8. Ping your device IP to confirm it's online.
9. Mount your ESP32 device close (recommend within ~1 meter for best performance) to your Halo Chlorinator and within WiFi network range.

# Installation

Best experience is to install with HACS.

[![Open your Home Assistant instance and open a repository inside the Home Assistant Community Store.](https://my.home-assistant.io/badges/hacs_repository.svg)](https://my.home-assistant.io/redirect/hacs_repository/?owner=DanielNagy&repository=astralpool_halo_chlorinator)

## Installation via HACS

1. Open the HACS page on your Home Assistant Dashboard.
2. Select "Integrations".
3. From the 3 dots menu, select "Custom Repositories".
4. Add the URL of this GitHub (https://github.com/DanielNagy/astralpool_halo_chlorinator). Select "Integration" as the Category.
5. Select "Astral Pool Halo Chlorinator". Download/install the latest version.
6. Restart HomeAssistant when instructed.

## Manual Installation

1. Using the tool of choice open the directory (folder) for your HA configuration (where you find `configuration.yaml`).
2. If you do not have a `custom_components` directory (folder) there, you need to create it.
3. In the `custom_components` directory (folder) create a new folder called `astralpool_halo_chlorinator`.
4. Download _all_ the files from the `custom_components/astralpool_halo_chlorinator/` directory (folder) in this repository.
5. Place the files you downloaded in the new directory (folder) you created.
6. Using your HA configuration directory (folder) as a starting point you should now also have this:

```text
custom_components/astralpool_halo_chlorinator/translations/en.json
custom_components/astralpool_halo_chlorinator/translations/fr.json
custom_components/astralpool_halo_chlorinator/translations/nb.json
custom_components/astralpool_halo_chlorinator/translations/sensor.en.json
custom_components/astralpool_halo_chlorinator/translations/sensor.fr.json
custom_components/astralpool_halo_chlorinator/translations/sensor.nb.json
custom_components/astralpool_halo_chlorinator/translations/sensor.nb.json
custom_components/astralpool_halo_chlorinator/__init__.py
custom_components/astralpool_halo_chlorinator/api.py
custom_components/astralpool_halo_chlorinator/binary_sensor.py
custom_components/astralpool_halo_chlorinator/config_flow.py
custom_components/astralpool_halo_chlorinator/const.py
custom_components/astralpool_halo_chlorinator/manifest.json
custom_components/astralpool_halo_chlorinator/sensor.py
custom_components/astralpool_halo_chlorinator/switch.py
```

7. Restart Home Assistant when instructed.

# Configuration

## Configuration is done in the Home Assistant UI

1. Visit your [HomeAssistant Integrations Dashboard](https://my.home-assistant.io/redirect/integrations)

[![Open your Home Assistant Integrations Dashboard.](https://my.home-assistant.io/badges/integrations.svg)](https://my.home-assistant.io/redirect/integrations/)

2. Wait patiently for your chlorinator to be discovered (should only be a few seconds once HA has started up)
3. When the Halo device is detected in Home Assistant, you will see a new HCHLOR integration card with button for 'Configure'.
4. Go to your physical Halo Control Panel (the one near your pool) to start the pairing process.

- Take a mobile device or laptop with you so you can control Home Assistant and the Chlorinator from the same place.

## Pair Your HALO

1. Open your Home Assistant Integrations page
2. Click the 'Configure' button on the newly discovered HCHLOR device.
3. Press submit to confirm 'add device'.
4. Home Assistant will start polling for new pairing connections.
5. On Halo Control Panel: Put your HALO into pairing mode.
6. On Home Assistant: Once discovered, Home Assistant will ask you what HA Area the Halo is located. Select your area as desired.
7. Your Halo should now be added to HA as 1 new device with ~19 entities.

Troubleshooting:

1. The HA pairing discovery may either error or the circle might just spin forever.
2. If it errors, hit config / add / confirm again (whilst the Halo is still in pairing mode).
3. If it is spinning, just wait approx 30 seconds, then cancel it, and hit configure again.
4. Repeat as needed until the pairing is successful.

# Note

Halo only supports one concurrent Bluetooth or Cloud connection at any point in time.  
While Home Assistant is polling your Halo, you will not be able to use your mobile app to connect to the Halo either via Bluetooth or Cloud.  
Likewise, while your mobile is connected, Home Assistant will not be able to poll the Halo.

If you need to access Halo from your mobile while Home Assistant is connected, you will have to wait for the poll to finish and then open your mobile connection.

- Open your mobile app and look for a 'blue dot' next to your chlorinator.
- If it is NOT there, HA is currently polling for data (takes 20 seconds to complete).
- As soon as the blue dot appears, you will be able to connect to it from your mobile.

# Other interesting links

## Hidden Menu

Halo has a hidden system menu that allows you to display the actual ORP value on the Halo screen and also on the app screen.
Here is a video on how to access the menu.
https://www.youtube.com/watch?v=zaRFVSt8Hc4

## Pool Monitor Card

https://github.com/wilsto/pool-monitor-card
The "Pool Monitor Card" is a home assistant plugin that display information of 12 pre-defined sensors of your swimming pool : temperature, pH, ORP levels and TDS but also if you need them : salinity, CYA, calcium, phosphate, alkalinity, free chlorine, total chlorine, filter pressure

<!---->

## Credits

This project was forked from [@pbutterworth](https://github.com/pbutterworth)'s' [AstralPool Chlorinator](https://github.com/pbutterworth/astralpool_chlorinator) with a future goal to merge both Halo and EQ together.

This project was generated from [@oncleben31](https://github.com/oncleben31)'s [Home Assistant Custom Component Cookiecutter](https://github.com/oncleben31/cookiecutter-homeassistant-custom-component) template.

Code template was mainly taken from [@Ludeeus](https://github.com/ludeeus)'s [integration_blueprint][integration_blueprint] template

---

[integration_blueprint]: https://github.com/custom-components/integration_blueprint
[black]: https://github.com/psf/black
[black-shield]: https://img.shields.io/badge/code%20style-black-000000.svg?style=for-the-badge
[commits-shield]: https://img.shields.io/github/commit-activity/y/DanielNagy/astralpool_halo_chlorinator.svg?style=for-the-badge
[commits]: https://github.com/DanielNagy/astralpool_halo_chlorinator/commits/main
[hacs]: https://hacs.xyz
[hacsbadge]: https://img.shields.io/badge/HACS-Custom-orange.svg?style=for-the-badge
[forum-shield]: https://img.shields.io/badge/community-forum-brightgreen.svg?style=for-the-badge
[forum]: https://community.home-assistant.io/
[license-shield]: https://img.shields.io/github/license/DanielNagy/astralpool_halo_chlorinator.svg?style=for-the-badge
[maintenance-shield]: https://img.shields.io/badge/maintainer-%40DanielNagy-blue.svg?style=for-the-badge
[pre-commit]: https://github.com/pre-commit/pre-commit
[pre-commit-shield]: https://img.shields.io/badge/pre--commit-enabled-brightgreen?style=for-the-badge
[releases-shield]: https://img.shields.io/github/release/DanielNagy/astralpool_halo_chlorinator.svg?style=for-the-badge
[releases]: https://github.com/DanielNagy/astralpool_halo_chlorinator/releases
[user_profile]: https://github.com/DanielNagy
[buymecoffee]: https://www.buymeacoffee.com/danielnagy
[buymecoffeebadge]: https://img.shields.io/badge/buy%20me%20a%20coffee-donate-yellow.svg?style=for-the-badge
