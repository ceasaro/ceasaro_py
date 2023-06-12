from handlers.json_handler import JSONHandler
from handlers.yaml_handler import YAMLHandler


class TranslatorFactory:
    handlers = [JSONHandler, YAMLHandler, ]

    def translate_file(self, file_path, target_lang, source_lang=None):

        handler_class = self.find_handler(file_path)
        if handler_class:
            handler = handler_class(file_path, target_lang, source_lang)
            handler.run_translation()
        else:
            print(f"No handler found for file {file_path}")

    def find_handler(self, file):
        for handler_class in self.handlers:
            if handler_class.can_handle(file):
                return handler_class

        # if file.endswith('.csv'):
        #     csv_handler.translate(file, columns_to_translate=[1, ])
        # if file.endswith('.yaml') or file.endswith('.yml'):
        #     yaml_handler.translate(file, target_lang)
        # if file.endswith('.json'):
        #     json_handler.translate(file, target_lang)
