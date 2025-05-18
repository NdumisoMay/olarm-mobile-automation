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