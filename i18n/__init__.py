import json
import os

_translations = {}
_i18n_dir = os.path.dirname(os.path.abspath(__file__))


def _load_translations():
    """Load all translation JSON files from the i18n directory."""
    global _translations
    for filename in os.listdir(_i18n_dir):
        if filename.endswith(".json"):
            lang_code = filename.replace(".json", "")
            filepath = os.path.join(_i18n_dir, filename)
            with open(filepath, "r", encoding="utf-8") as f:
                _translations[lang_code] = json.load(f)


def t(key: str, lang: str = "en") -> str:
    """Get a translated string by key and language.

    Args:
        key: The translation key (e.g. 'app_title', 'search_placeholder').
        lang: Language code (e.g. 'en', 'zh_tw', 'ja').

    Returns:
        The translated string, or the key itself as fallback.
    """
    if not _translations:
        _load_translations()

    lang_dict = _translations.get(lang, _translations.get("en", {}))
    return lang_dict.get(key, _translations.get("en", {}).get(key, key))


def get_all(lang: str = "en") -> dict:
    """Get all translations for a given language.

    Args:
        lang: Language code.

    Returns:
        A dict of all key-value translation pairs.
    """
    if not _translations:
        _load_translations()

    return _translations.get(lang, _translations.get("en", {}))
