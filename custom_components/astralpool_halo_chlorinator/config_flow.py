"""Config flow for Astral Pool Viron eQuilibrium and Halo Chlorinator integration."""
from __future__ import annotations

import asyncio
import logging
from typing import Any

from bluetooth_data_tools import human_readable_name
from pychlorinator.halo_parsers import ScanResponse
import voluptuous as vol

from homeassistant import config_entries
from homeassistant.components.bluetooth import (
    BluetoothScanningMode,
    BluetoothServiceInfoBleak,
    async_discovered_service_info,
    async_process_advertisements,
)
from homeassistant.const import CONF_ACCESS_TOKEN, CONF_ADDRESS
from homeassistant.data_entry_flow import FlowResult

from .const import DOMAIN, LOCAL_NAMES

_LOGGER = logging.getLogger(__name__)

# number of seconds to wait for a device to be put in pairing mode
WAIT_FOR_PAIRING_TIMEOUT = 20


class ConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Handle a config flow for eQuilibrium Chlorinator."""

    VERSION = 1

    def __init__(self) -> None:
        """Initialize the config flow."""
        self._discovery_info: BluetoothServiceInfoBleak | None = None
        self._discovered_devices: dict[str, BluetoothServiceInfoBleak] = {}
        self._pairing_task: asyncio.Task | None = None
        self._bytes_access_code: None

    async def async_step_bluetooth(
        self, discovery_info: BluetoothServiceInfoBleak
    ) -> FlowResult:
        """Handle the bluetooth discovery step."""
        await self.async_set_unique_id(discovery_info.address)
        self._abort_if_unique_id_configured()
        self._discovery_info = discovery_info
        self.context["title_placeholders"] = {
            "name": human_readable_name(
                None, discovery_info.name, discovery_info.address
            )
        }
        if discovery_info.name == "HCHLOR":
            return await self.async_step_halo_bluetooth_confirm()
        return await self.async_step_user()

    async def async_step_halo_bluetooth_confirm(
        self, user_input: dict[str, Any] | None = None
    ) -> FlowResult:
        """Confirm discovery."""
        assert self._discovery_info is not None

        if user_input is not None:
            if getattr(self._discovery_info, "manufacturer_data", None) is not None:
                # manufacturer_data exists - Appears to be a bleak bug that sometimes doesnt show manufacturer data
                manufacturer_data = self._discovery_info.manufacturer_data[1095]
                if not ScanResponse(manufacturer_data).isPairable:
                    return await self.async_step_wait_for_pairing_mode()
                # return self._discovery_info.name

        self._set_confirm_only()
        assert self._discovery_info.name
        placeholders = {"name": self._discovery_info.name}
        self.context["title_placeholders"] = placeholders
        return self.async_show_form(
            step_id="halo_bluetooth_confirm", description_placeholders=placeholders
        )

    async def async_step_wait_for_pairing_mode(
        self, user_input: dict[str, Any] | None = None
    ) -> FlowResult:
        """Wait for device to enter pairing mode."""
        if not self._pairing_task:
            self._pairing_task = self.hass.async_create_task(
                self._async_wait_for_pairing_mode()
            )

        if not self._pairing_task.done():
            return self.async_show_progress(
                step_id="wait_for_pairing_mode",
                progress_action="wait_for_pairing_mode",
                progress_task=self._pairing_task,
            )

        try:
            await self._pairing_task
        except asyncio.TimeoutError:
            return self.async_show_progress_done(next_step_id="pairing_timeout")
        finally:
            self._pairing_task = None

        return self.async_show_progress_done(next_step_id="pairing_complete")

    async def async_step_pairing_complete(
        self, user_input: dict[str, Any] | None = None
    ) -> FlowResult:
        """Create a configuration entry for a device that entered pairing mode."""
        _LOGGER.info("async_step_pairing_complete")

        assert self._discovery_info.name

        _LOGGER.info(
            "Pair complete - access code: %s\n  Address: %s",
            self._bytes_access_code,
            self._discovery_info.address,
        )

        await self.async_set_unique_id(
            self._discovery_info.address, raise_on_progress=False
        )
        self._abort_if_unique_id_configured()

        return self.async_create_entry(
            title=self._discovery_info.name,
            data={
                CONF_ADDRESS: self._discovery_info.address,
                CONF_ACCESS_TOKEN: self._bytes_access_code,
            },
        )

    async def async_step_pairing_timeout(
        self, user_input: dict[str, Any] | None = None
    ) -> FlowResult:
        """Inform the user that the device never entered pairing mode."""
        if user_input is not None:
            return await self.async_step_wait_for_pairing_mode()

        self._set_confirm_only()
        return self.async_show_form(step_id="pairing_timeout")

    async def _async_wait_for_pairing_mode(self) -> None:
        """Process advertisements until pairing mode is detected."""
        assert self._discovery_info
        _LOGGER.info("_async_wait_for_pairing_mode")

        def is_device_in_pairing_mode(
            service_info: BluetoothServiceInfoBleak,
        ) -> bool:
            manufacturer_data = service_info.manufacturer_data[1095]
            self._bytes_access_code = ScanResponse(manufacturer_data).get_access_code()
            _LOGGER.info("Access Code %s", self._bytes_access_code)
            return ScanResponse(manufacturer_data).isPairable

        await async_process_advertisements(
            self.hass,
            is_device_in_pairing_mode,
            {"address": self._discovery_info.address},
            BluetoothScanningMode.ACTIVE,
            WAIT_FOR_PAIRING_TIMEOUT,
        )

    """ Below is EQ """

    async def async_step_user(
        self, user_input: dict[str, Any] | None = None
    ) -> FlowResult:
        """Handle the user step to pick discovered device."""
        errors: dict[str, str] = {}
        if user_input is not None:
            address = user_input[CONF_ADDRESS]
            accesscode = user_input[CONF_ACCESS_TOKEN]
            discovery_info = self._discovered_devices[address]
            local_name = discovery_info.name
            await self.async_set_unique_id(
                discovery_info.address, raise_on_progress=False
            )
            self._abort_if_unique_id_configured()
            return self.async_create_entry(
                title=local_name,
                data={
                    CONF_ADDRESS: discovery_info.address,
                    CONF_ACCESS_TOKEN: accesscode,
                },
            )

        if discovery := self._discovery_info:
            self._discovered_devices[discovery.address] = discovery
        else:
            current_addresses = self._async_current_ids()
            for discovery in async_discovered_service_info(self.hass):
                if (
                    discovery.address in current_addresses
                    or discovery.address in self._discovered_devices
                    or not any(
                        discovery.name.startswith(local_name)
                        for local_name in LOCAL_NAMES
                    )
                ):
                    continue
                self._discovered_devices[discovery.address] = discovery

        if not self._discovered_devices:
            return self.async_abort(reason="no_unconfigured_devices")

        data_schema = vol.Schema(
            {
                vol.Required(CONF_ADDRESS): vol.In(
                    {
                        service_info.address: f"{service_info.name} ({service_info.address})"
                        for service_info in self._discovered_devices.values()
                    }
                ),
                vol.Required(CONF_ACCESS_TOKEN, description="CONF_ACCESS_TOKEN"): str,
            }
        )
        return self.async_show_form(
            step_id="user",
            data_schema=data_schema,
            errors=errors,
        )
