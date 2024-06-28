from typing import *
import os
import glob
import time
import traceback
from threading import Thread
from datetime import timedelta, datetime, timezone
from django.utils import timezone as dj_timezone

from ..conf import settings
from ..signals import resource_changed
from . import registry


def monitor(
    delta: timedelta = settings.CHECK_DELTA,
    now: Optional[datetime] = None,
):
    now = now if now is not None else dj_timezone.now()

    for key, patterns, handler in registry.items():
        found = (
            (path, p)
            for p in patterns
            for path in glob.iglob(p, recursive=True)
            if datetime.fromtimestamp(
                os.stat(path, follow_symlinks=True).st_mtime,
                tz=timezone.utc,
            ) + delta > now
        )
        changed, pattern = next(found, (None, None))

        if changed is None:
            continue

        handler(key, changed, pattern)
        resource_changed.send(None, ke=key, changed=changed, pattern=pattern)


def monitor_thread_runner(delta: timedelta = settings.CHECK_DELTA):
    while 1:
        try:
            monitor(delta=delta)
        except Exception as e:
            traceback.print_exception(e)
        time.sleep(delta.total_seconds() * 0.95)


def schedule_monitor(delta: timedelta = settings.CHECK_DELTA):
    thread = Thread(
        target=monitor_thread_runner,
        kwargs={'delta': delta},
        daemon=True,
    )
    thread.start()
