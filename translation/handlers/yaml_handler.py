import yaml
import json

import deepl_api
from utils.trans_utils import translate_dict

from .abstract_handler import TranslateHandler


class YAMLHandler(TranslateHandler):

    @classmethod
    def can_handle(cls, file_path):
        return file_path.endswith('.yaml') or file_path.endswith('.yml')

    def translate(self):
        """
        write the data of a single simulation to the provided stream
        """
        print('yaml translation')
        with open(self.file_path) as f:
            data = yaml.safe_load(f)

        translated_dict = translate_dict(data, self.target_lang)
        return yaml.dump(translated_dict)
