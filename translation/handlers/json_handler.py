import json

import deepl_api

from .abstract_handler import TranslateHandler


class JSONHandler(TranslateHandler):

    @classmethod
    def can_handle(cls, file_path):
        return file_path.endswith('.json')

    def translate(self):
        """
        write the data of a single simulation to the provided stream
        """
        with open(self.file_path) as f:
            json_data = json.loads(f.read())

        translated_dict = self.translate_dict(json_data, self.target_lang)
        translated_json = json.dumps(translated_dict)
        return translated_json

    def translate_dict(self, a_dict, target_lang):
        for key, value in a_dict.items():
            if type(value) is dict:
                a_dict[key] = self.translate_dict(value, target_lang)
            elif type(value) is str:
                a_dict[key] = deepl_api.translate_text(value, target_lang)
        return a_dict

