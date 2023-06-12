import deepl_api


def translate_dict(a_dict, target_lang):
    for key, value in a_dict.items():
        if type(value) is dict:
            a_dict[key] = translate_dict(value, target_lang)
        elif type(value) is str:
            a_dict[key] = deepl_api.translate_text(value, target_lang)
    return a_dict
