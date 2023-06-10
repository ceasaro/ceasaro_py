import os


class TranslateHandler:
    def __init__(self, file_path, target_lang, source_lang=None):
        self.file_path = file_path
        self.target_lang = target_lang
        self.source_lang = source_lang
        self.filename, self.file_extension = os.path.splitext(self.file_path)

    @classmethod
    def can_handle(cls, file_path):
        return False

    def run_translation(self):
        print(f"translating {self.file_path} from {self.source_lang} to {self.target_lang}, using {self.__class__.__name__}")
        translated_content = self.translate()
        self.write_file(translated_content)

    def translate(self):
        pass

    def write_file(self, content):
        new_file_name = f"{self.filename}-{self.target_lang}{self.file_extension}"
        file1 = open(new_file_name, 'w')
        file1.write(content)
        file1.close()
        print(f"translated file written to {new_file_name}")