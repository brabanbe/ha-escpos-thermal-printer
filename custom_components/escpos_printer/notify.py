from __future__ import annotations

import logging

from homeassistant.components.notify import NotifyEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from typing import Any

from .const import DOMAIN

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry, async_add_entities) -> None:
    _LOGGER.debug("Setting up notify entity for entry %s", entry.entry_id)
    async_add_entities([EscposNotifyEntity(hass, entry)])


class EscposNotifyEntity(NotifyEntity):
    """Notification entity for ESC/POS thermal printer.

    Provides Home Assistant notification integration that prints messages
    to the configured thermal printer.
    """

    _attr_has_entity_name = True

    def __init__(self, hass: HomeAssistant, entry: ConfigEntry) -> None:
        """Initialize the notification entity.

        Args:
            hass: Home Assistant instance
            entry: Config entry for the printer
        """
        self._hass = hass
        self._entry = entry
        self._attr_name = f"ESC/POS Printer {entry.title}"
        self._attr_unique_id = f"{entry.entry_id}_notify"

    async def async_send_message(self, message: str = "", **kwargs: Any) -> None:
        """Send a notification message to the thermal printer.

        Args:
            message: The message content to print
            **kwargs: Additional notification parameters including:
                - title: Optional title to print before the message
                - data: Optional data dictionary with printer-specific options
        """
        _LOGGER.debug(
            "Notify send_message called: title=%s, message_len=%s, data_keys=%s",
            kwargs.get("title"),
            len(message or ""),
            list((kwargs.get("data") or {}).keys()),
        )
        title = kwargs.get("title")
        data = kwargs.get("data") or {}
        defaults = self._hass.data[DOMAIN][self._entry.entry_id]["defaults"]
        adapter = self._hass.data[DOMAIN][self._entry.entry_id]["adapter"]

        text = f"{title}\n{message}" if title else message
        try:
            await adapter.print_text(
                self._hass,
                text=text,
                align=defaults.get("align"),
                bold=False,
                underline="none",
                width=1,
                height=1,
                density=9,
                encoding=None,
                cut=data.get("cut", defaults.get("cut")),
                feed=data.get("feed", 0),
                invert=False,
                flip=False,
                smooth=False,

            )
        except Exception as err:  # Bubble up to notify error handling
            _LOGGER.error("print_text failed: %s", err)
            raise
