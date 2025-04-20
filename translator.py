import json

class Translator:
    def __init__(self, translations_file="translations.json"):
        with open(translations_file, "r", encoding="utf-8") as f:
            self.translations = json.load(f)
        self.default_lang = "ru"

    def get_text(self, text_id, lang=None, **kwargs):
        if lang is None:
            lang = self.default_lang
        text = self.translations.get(lang, {}).get(text_id, f"[{text_id}]")
        try:
            return text.format(**kwargs) if kwargs else text
        except KeyError as e:
            return f"[{text_id}: missing {str(e)}]"