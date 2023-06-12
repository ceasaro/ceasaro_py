import json

import deepl_api
from utils.trans_utils import translate_dict

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

        translated_dict = translate_dict(json_data, self.target_lang)
        return json.dumps(translated_dict)
