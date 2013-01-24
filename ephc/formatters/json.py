import json

import ephc.healthchecks as healthchecks


class JsonFormatter(object):
    def __init__(self, input):
        self.input = input
        
    def format(self):
        output = json.dumps(self.input)
        
        return output