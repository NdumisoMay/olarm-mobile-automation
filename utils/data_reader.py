import json
import os

def read_test_data(key):
    file_path = os.path.join(os.path.dirname(__file__), '../testdata/login_data.json')
    with open(file_path) as f:
        data = json.load(f)
    return data.get(key)

def read_device_details(key):
    file_path = os.path.join(os.path.dirname(__file__), '../testdata/olarm_device_data.json')
    with open(file_path) as f:
        data = json.load(f)
    return data.get(key)


def read_sql_injection_data(key):
    file_path = os.path.join(os.path.dirname(__file__), '../testdata/sql_injection_data.json')
    with open(file_path) as f:
        data = json.load(f)
    result = data.get(key)
    if result is None:
        raise ValueError(f"No data found for key: {key}")
    if not isinstance(result, list):
        raise TypeError(f"Expected list for key '{key}', but got {type(result).__name__}")
    return result

def read_cell_no_data(key):
    file_path = os.path.join(os.path.dirname(__file__), '../testdata/phone_no_data.json')
    with open(file_path) as f:
        data = json.load(f)
    result = data.get(key)
    if result is None:
        raise ValueError(f"No data found for key: {key}")
    if not isinstance(result, list):
        raise TypeError(f"Expected list for key '{key}', but got {type(result).__name__}")
    return result