import gettext
from pathlib import Path

from fastapi import Request


class TranslationWrapper:
    """
        Singleton responsible for translated messages based on locale
    """
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance.init_translation()
        return cls._instance

    def init_translation(self):
        """
        Init translations based on default language and translation files
        :return:
        """
        lang = "en"  # Default language
        # i18n\translations
        locales_dir = Path(__file__).parent / "translations"
        self.translations = gettext.translation(
            "messages",
            localedir=locales_dir,
            languages=[lang],
            fallback=True
        )
        self.translations.install()

    def gettext(self, message: str) -> str:
        """
        Get translated message
        :param message: original message
        :return: translated version
        """
        return self.translations.gettext(message)


async def set_locale(request: Request):
    """
    Set translations langauge based on Accept-Language header
    :param request: http request
    :return:
    """
    translation_wrapper = TranslationWrapper()

    lang = request.headers.get("Accept-Language", "en")
    locales_dir = Path(__file__).parent / "translations"

    translation_wrapper.translations = gettext.translation(
        "messages", localedir=locales_dir, languages=[lang], fallback=True
    )

    translation_wrapper.translations.install()


def _(message: str) -> str:
    """
    Wrapper for getting the translated message in application
    :param message: original message
    :return: translated message
    """
    translation_wrapper = TranslationWrapper()
    return translation_wrapper.gettext(message)
