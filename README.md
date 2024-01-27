# Astral Pool Halo Chlorinator

### No Affiliation with Astral Pools or Fluindra

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

## Installation

1. Using the tool of choice open the directory (folder) for your HA configuration (where you find `configuration.yaml`).
2. If you do not have a `custom_components` directory (folder) there, you need to create it.
3. In the `custom_components` directory (folder) create a new folder called `astralpool_halo_chlorinator`.
4. Download _all_ the files from the `custom_components/astralpool_halo_chlorinator/` directory (folder) in this repository.
5. Place the files you downloaded in the new directory (folder) you created.
6. Restart Home Assistant
7. Wait paitently for your chlorinator to be discovered (should only be a few seconds once HA has started up)
8. Upon discovery, you will need to manually enter Pair mode in the Halo's settings.

Using your HA configuration directory (folder) as a starting point you should now also have this:

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

## Configuration is done in the UI

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
