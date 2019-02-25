import json


class message:

    def convert(self, data, action = 'byte_to_json', unicode = 'utf-8'):
        if action == "byte_to_json":
            json_ = data.decode('utf8').replace("'", '"')
            data_ = json.loads(json_)
            return json.dumps(data_, indent=4, sort_keys=True)
        elif action == "json_to_byte":
            text = json.dumps(data)
            return bytes(text, unicode)
        pass

    def show(self, value_color="", value_noncolor=""):
        HEADER = '\033[92m'
        ENDC = '\033[0m'
        print(HEADER + value_color + ENDC + str(value_noncolor))
