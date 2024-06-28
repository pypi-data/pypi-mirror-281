from pythed.app.utils import config_functions

def get_all_status():
    try:
        return config_functions.read_json("../config/status.json")
    except Exception as e:
        print(e)