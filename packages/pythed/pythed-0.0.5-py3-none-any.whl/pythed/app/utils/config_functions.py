import json
import pkg_resources

def read_json(file_path):
    data_path = pkg_resources.resource_filename(__name__, file_path)
    with open(data_path, 'r', encoding='utf-8') as f:
        return json.load(f)