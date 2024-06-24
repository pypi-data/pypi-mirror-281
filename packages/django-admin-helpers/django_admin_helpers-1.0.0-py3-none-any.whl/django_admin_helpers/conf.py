"""
These are the available settings.

All attributes prefixed ``ADMIN_HELPERS_*`` can be overridden from your Django
project's settings module by defining a setting with the same name.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from django.conf import settings as django_settings

# All attributes accessed with this prefix are possible to overwrite
# through django.conf.settings.
SETTINGS_PREFIX = "ADMIN_HELPERS_"


@dataclass(frozen=True)
class AppSettings:
    """Access this instance as `.conf.app_settings`."""

    ADMIN_HELPERS_URL_NAMESPACE: str = "admin"
    """URL namespace for the admin app (defaults to 'admin')."""

    def __getattribute__(self, __name: str) -> Any:
        """
        Check if a Django project settings should override the app default.

        In order to avoid returning any random properties of the django settings,
        we inspect the prefix firstly.
        """
        if __name.startswith(SETTINGS_PREFIX) and hasattr(django_settings, __name):
            return getattr(django_settings, __name)

        return super().__getattribute__(__name)


app_settings = AppSettings()
