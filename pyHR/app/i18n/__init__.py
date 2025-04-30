import gettext
from pathlib import Path
from fastapi import Request


class TranslationWrapper:

    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance.init_translation()
        return cls._instance

    def init_translation(self):
        lang = "en"  # Default language
        # src/translation
        locales_dir = Path(__file__).parent / "translations"
        self.translations = gettext.translation(
            "messages",
            localedir=locales_dir,
            languages=[lang],
            fallback=True
        )
        self.translations.install()

    def gettext(self, message: str) -> str:
        return self.translations.gettext(message)


async def set_locale(request: Request):
    translation_wrapper = TranslationWrapper()

    lang = request.headers.get("Accept-Language", "en")
    locales_dir = Path(__file__).parent / "translations"

    translation_wrapper.translations = gettext.translation(
        "messages", localedir=locales_dir, languages=[lang], fallback=True
    )

    translation_wrapper.translations.install()


def _(message: str) -> str:
    translation_wrapper = TranslationWrapper()
    return translation_wrapper.gettext(message)