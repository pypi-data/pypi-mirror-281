from django.apps import AppConfig
from django.utils.translation import pgettext_lazy


class TranslationsMonitorConfig(AppConfig):
    name = 'wcd_filemonitor.contrib.translations'
    label = 'wcd_filemonitor_translations'
    verbose_name = pgettext_lazy('wcd_filemonitor', 'Translations monitor')
    default_auto_field = 'django.db.models.AutoField'

    def ready(self) -> None:
        super().ready()
        from systems.wcd_filemonitor.services import registry
        from . import resolver

        registry.add(
            'translations',
            resolver.make_globs(),
            resolver.handle_change,
        )
