from pathlib import Path
from django.conf import settings
import traceback


__all__ = (
    'make_globs',
    'handle_change',
    'reset_translation_cache',
)


def make_globs():
    return [str(Path(p) / '**' / '*.po') for p in settings.LOCALE_PATHS]


def handle_change(key: str, file: str, pattern: str):
    reset_translation_cache()


def reset_translation_cache():
    from django.utils.translation import trans_real
    from django.conf import settings
    import gettext

    if settings.USE_I18N:
        try:
            # Reset gettext.GNUTranslation cache.
            gettext._translations = {}

            # Reset Django by-language translation cache.
            trans_real._translations = {}

            # Delete Django current language translation cache.
            trans_real._default = None
        except AttributeError as e:
            traceback.print_exception(e)
