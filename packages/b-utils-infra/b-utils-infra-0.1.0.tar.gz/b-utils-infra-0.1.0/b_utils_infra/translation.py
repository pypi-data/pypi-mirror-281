from typing import Literal

import deepl
import six
from b_utils_infra.generic import retry_with_timeout
from google.cloud import translate_v2 as google_translate


class TextTranslator:
    """
    for google translate, set GOOGLE_APPLICATION_CREDENTIALS env variable
    to the path of the google service account json file before using this class
    os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = join(current_path, 'google_service_account.json')
    """

    def __init__(self, deepl_api_key: str, languages: list[str]):
        self.google_translate_client = google_translate.Client()
        self.deepl_translate_client = deepl.Translator(deepl_api_key)
        self.languages = languages

    @retry_with_timeout(retries=3, timeout=120, initial_delay=20, backoff=2)
    def translate_text_with_google(self, text_to_translate, target_lang, source_language):
        """Translates text into the target language.

        Target must be an ISO 639-1 language code.
        See https://g.co/cloud/translate/v2/translate-reference#supported_languages
        """

        if isinstance(text_to_translate, six.binary_type):
            text_to_translate = text_to_translate.decode("utf-8")

        result = self.google_translate_client.translate(text_to_translate,
                                                        target_language=target_lang,
                                                        source_language=source_language)

        return result["translatedText"]

    @retry_with_timeout(retries=2, timeout=120, initial_delay=30, backoff=2)
    def translate_text_with_deepl(self,
                                  text_to_translate: str,
                                  source_lang: str,
                                  target_lang: str,
                                  tag_handling: str = None):
        result = self.deepl_translate_client.translate_text(
            text=text_to_translate,
            source_lang=source_lang.upper(),
            target_lang=target_lang,
            tag_handling=tag_handling
        )
        # The result is a list of TextResult objects, or a single TextResult object if the text was one string.
        if isinstance(result, list):
            return result[0].text
        return result.text

    def get_translations(self,
                         text_: str,
                         replace_lang_url: bool = False,
                         source_language: Literal["en", "ru", "ar", "de", "es", "fr", "uk"] = "en",
                         target_langs: list[Literal["ru", "ar", "de", "es", "fr", "uk"]] = None,
                         engine: Literal["google", "deepl"] = "google",
                         tag_handling: str = None) -> dict[str, str]:
        """
        Translate text to all languages in LANGUAGES dict
        :param text_: text to translate
        :param replace_lang_url: replace base url with the base url from target language in the text.
        :param source_language: source language ['en', 'ru', 'ar', 'de', 'es', 'fr', 'uk']
        :param target_langs: list of languages to translate to, if None, translate to all languages in LANGUAGES dict
        :param engine: the translation engine to use, either "google" or "deepl"
        :param tag_handling: for deepl only, how to handle tags in the text, either "xml" or "html"
        :return: dict with translations
        """
        if engine and engine not in ["google", "deepl"]:
            raise ValueError("engine must be either 'google' or 'deepl'")
        if source_language not in ['en', 'ru', 'ar', 'de', 'es', 'fr', 'uk']:
            raise ValueError("source_language must be one of 'en', 'ru', 'ar', 'de', 'es', 'fr', 'uk'")
        if target_langs and not all(lang in self.languages for lang in target_langs):
            raise ValueError("target_langs must be a list of 'ru', 'ar', 'de', 'es', 'fr', 'uk'")

        translations = {'en': text_}
        if not text_:
            return translations

        for lang in self.languages:
            if target_langs and lang not in target_langs:
                continue
            if engine == "google":
                translated_text = self.translate_text_with_google(
                    text_to_translate=text_,
                    target_lang=lang,
                    source_language=source_language
                )
            elif engine == "deepl":
                translated_text = self.translate_text_with_deepl(
                    text_to_translate=text_,
                    source_lang=source_language,
                    target_lang=lang,
                    tag_handling=tag_handling
                )
            else:
                raise ValueError("engine must be either 'google' or 'deepl'")

            if replace_lang_url:
                translated_text = translated_text.replace('https://us-uk.bookimed.com/',
                                                          self.languages[lang])

            if lang == 'uk':
                lang = 'ua'

            translations[lang] = translated_text

        return translations
