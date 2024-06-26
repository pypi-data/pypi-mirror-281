# -*- encoding: utf-8 -*-
import gettext
import locale
import os

__all__ = ["_"]

xba2l_LANGUAGE_KEY = "xba2l_LANGUAGE"

DOMAIN = "xba2l"
LOCALE_DIR = "xba2l/i18n"

LANGUAGES = os.environ[xba2l_LANGUAGE_KEY].split(";") if xba2l_LANGUAGE_KEY in os.environ else locale.getlocale()

if gettext.find(DOMAIN, localedir=LOCALE_DIR, languages=LANGUAGES):
    es: gettext.GNUTranslations = gettext.translation(DOMAIN, localedir=LOCALE_DIR, languages=LANGUAGES)
    es.install()
    _ = es.gettext
else:
    _ = gettext.gettext
