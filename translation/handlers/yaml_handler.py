import yaml


def translate(yaml_file_path, target_lang):
    """
    write the data of a single simulation to the provided stream
    """
    print('yaml translation')
    with open(yaml_file_path) as f:
        data = yaml.load(f)

    print(data)