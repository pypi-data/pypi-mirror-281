from typing import *
from dataclasses import dataclass
from datetime import timedelta

from px_settings.contrib.django import settings as setting_wrap


__all__ = 'SETTINGS_PREFIX', 'Settings', 'settings',

SETTINGS_PREFIX = 'WCD_FILEMONITOR'


@setting_wrap(SETTINGS_PREFIX)
@dataclass
class Settings:
    CHECK_DELTA: timedelta = timedelta(minutes=5)


settings = Settings()
