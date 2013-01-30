"""a space delimited key/value of pass/fail

servicemix 1
hmdb 0
unclemomspopshop 1
...

write it to stdout
"""

class BashMon(object):
    
    def __init__(self, input):
        self.input = input
        
    def get_results(self):
        summary = []
        for section in self.input:
            for subsection in self.input[section]:
                name = subsection
                status = self.input[section][subsection]['Success']
                summary.append((name, status))
            
        return summary
        
    def format(self):
        for service in self.get_results():
            print service[0], service[1]