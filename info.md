[![GitHub Release][releases-shield]][releases]
[![GitHub Activity][commits-shield]][commits]
[![License][license-shield]][license]

[![hacs][hacsbadge]][hacs]
[![Project Maintenance][maintenance-shield]][user_profile]

[![Community Forum][forum-shield]][forum]

[![BuyMeCoffee][buymecoffeebadge]][buymecoffee]

**This component will set up the following platforms.**

| Platform        | Description                                      |
| --------------- | ------------------------------------------------ |
| `binary_sensor` | Show something `True` or `False`.                |
| `sensor`        | Show info from Astral Pool Halo Chlorinator API. |
| `select`        | Control the chlorinator mode (off/auto/manual)   |

{% if not installed %}

## Installation

1. Click install.
1. Home Assistant will now discover chlorinators in bluetooth range that are advertising the right BLE UUID

{% endif %}

## Configuration is done in the UI

<!---->

## Credits

This project was forked from [@pbutterworth](https://github.com/pbutterworth)'s' [AstralPool Chlorinator](https://github.com/pbutterworth/astralpool_chlorinator) with a future goal to merge both Halo and EQ together.

This project was generated from [@oncleben31](https://github.com/oncleben31)'s [Home Assistant Custom Component Cookiecutter](https://github.com/oncleben31/cookiecutter-homeassistant-custom-component) template.

Code template was mainly taken from [@Ludeeus](https://github.com/ludeeus)'s [integration_blueprint][integration_blueprint] template

---

[integration_blueprint]: https://github.com/custom-components/integration_blueprint
[commits-shield]: https://img.shields.io/github/commit-activity/y/pbutterworth/astralpool_chlorinator.svg?style=for-the-badge
[commits]: https://github.com/pbutterworth/astralpool_chlorinator/commits/main
[hacs]: https://hacs.xyz
[hacsbadge]: https://img.shields.io/badge/HACS-Custom-orange.svg?style=for-the-badge
[forum-shield]: https://img.shields.io/badge/community-forum-brightgreen.svg?style=for-the-badge
[forum]: https://community.home-assistant.io/
[license]: https://github.com/pbutterworth/astralpool_chlorinator/blob/main/LICENSE
[license-shield]: https://img.shields.io/github/license/pbutterworth/astralpool_chlorinator.svg?style=for-the-badge
[maintenance-shield]: https://img.shields.io/badge/maintainer-%40pbutterworth-blue.svg?style=for-the-badge
[releases-shield]: https://img.shields.io/github/release/pbutterworth/astralpool_chlorinator.svg?style=for-the-badge
[releases]: https://github.com/pbutterworth/astralpool_chlorinator/releases
[user_profile]: https://github.com/pbutterworth
[buymecoffee]: https://www.buymeacoffee.com/pbutterworQ
[buymecoffeebadge]: https://img.shields.io/badge/buy%20me%20a%20coffee-donate-yellow.svg?style=for-the-badge
