#https://stackoverflow.com/questions/40059654/python-convert-a-bytes-array-into-json-format
import json


class Message:
    def __init__(self):
        pass

    def convert(self, data, action = 'byte_to_json', unicode = 'utf-8'):
        if action == "byte_to_json":
            json_ = data.decode('utf8').replace("'", '"')
            data_ = json.loads(json_)
            return json.dumps(data_, indent=4, sort_keys=True)
        elif action == "json_to_byte":
            text = json.dumps(data)
            return bytes(text, unicode)
        pass

