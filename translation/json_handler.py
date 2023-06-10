import json

import deepl_api


def translate(yaml_file_path, target_lang):
    """
    write the data of a single simulation to the provided stream
    """
    print('json translation')
    with open(yaml_file_path) as f:
        json_data = json.loads(f.read())

    translated_dict = translate_dict(json_data, target_lang)
    print(json.dumps(translated_dict))


def translate_dict(a_dict, target_lang):
    for key, value in a_dict.items():
        if type(value) is dict:
            a_dict[key] = translate_dict(value, target_lang)
        elif type(value) is str:
            a_dict[key] = deepl_api.translate_text(value, target_lang)
    return a_dict

