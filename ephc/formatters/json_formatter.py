import json


class JsonFormatter(object):
    def __init__(self, input):
        self.input = input
        
    def format(self):
        output = json.dumps(self.input)
        
        return output