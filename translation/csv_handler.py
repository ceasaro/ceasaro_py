import deepl_api

import unicodecsv


def translate(csv_file_path, columns_to_translate=None, has_header=False, encoding='UTF-8', sep=',', quote_char='"'):
    """
    write the data of a single simulation to the provided stream
    """
    with open(csv_file_path, 'rb') as csv_file:
        reader = unicodecsv.reader(csv_file,
                                   encoding=encoding,
                                   delimiter=sep,
                                   quotechar=quote_char)
        if has_header:
            header = next(reader, [])
        for row in reader:
            if columns_to_translate is None:
                columns_to_translate = range(len(row))
            output = ''
            for column_index in columns_to_translate:
                translated = ''
                deeple_json = deepl_api.translate(row[column_index], target_lang='BE', source_lang='FR')
                if deeple_json:
                    translations = deeple_json.get('translations', [])
                    translated = ','.join(t.get('text') for t in translations)

                output = f"{output}{',' if output else ''}{translated}"
            print(output)
