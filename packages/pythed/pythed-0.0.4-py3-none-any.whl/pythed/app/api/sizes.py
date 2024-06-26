from pythed.app.utils import config_functions

def get_all_sizes():
    try:
        return config_functions.read_json("../config/sizes.json")
    except Exception as e:
        print(e)