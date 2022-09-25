# curl -X POST 'https://api-free.deepl.com/v2/translate' \
# 	-H 'Authorization: DeepL-Auth-Key [yourAuthKey]' \
# 	-d 'text=Hello%2C%20world!' \
# 	-d 'target_lang=DE'
#
import requests

DEEPL_DOMAIN = "https://api-free.deepl.com"
DEEPL_VERSION = "v2"
DEEPL_TOKEN = "37009457-c483-0947-1d70-823a6f80e4c2:fx"

DEEPL_URL = f"{DEEPL_DOMAIN}/{DEEPL_VERSION}"

session = requests.session()


def __get(path, params=None):
    resp = session.get(
        f"{DEEPL_URL}/{path}",
        params=params,
        headers={'Authorization': 'DeepL-Auth-Key {}'.format(DEEPL_TOKEN)}
    )
    return resp


def translate(to_translate, target_lang, source_lang=None):
    """
    Deppl documentation see https://www.deepl.com/docs-api/translate-text/
    :param to_translate:
    :param target_lang:
    :return:
    """
    params = {'text': to_translate, 'target_lang': target_lang}
    if source_lang:
        params['source_lang'] = source_lang
    resp = __get(path='translate', params=params)
    if resp.status_code == 200:
        return resp.json()
