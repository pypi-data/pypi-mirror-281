from django.apps import AppConfig
from django.utils.translation import pgettext_lazy


class FileMonitorConfig(AppConfig):
    name = 'wcd_filemonitor'
    label = 'wcd_filemonitor'
    verbose_name = pgettext_lazy('wcd_filemonitor', 'File monitor')
    default_auto_field = 'django.db.models.AutoField'

    def ready(self) -> None:
        super().ready()
        from .services import monitor

        monitor.schedule_monitor()
