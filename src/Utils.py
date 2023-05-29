import json


class APIResponse:
    def __init__(self, data, status_code, message):
        self.status_code = status_code
        self.message = message
        self.data = data

    def to_json(self):
        response = {
            'status_code': self.status_code,
            'message': self.message,
            'data': self.data
        }
        return json.dumps(response)
