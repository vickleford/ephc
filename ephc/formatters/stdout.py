import os


class StdoutFormatter(object):
    def __init__(self, in_dict):
        self.in_dict = in_dict
        
    def format(self):
        rows, columns = os.popen('stty size', 'r').read().split()
        for title in self.in_dict:
            #print "{0:^int(self.columns)}".format(title)
            print "__________{0}__________".format(title)
            
            for section in self.in_dict[title]:
                print "{sect}...".format(sect=section),
                print self.in_dict[title][section]['Reason']
                result = "{success} ({elapsed}s)".format(
                    success=self.in_dict[title][section]['Success'],
                    elapsed=self.in_dict[title][section]['Elapsed'])
                print "{result:>{cols}}".format(result=result, cols=columns)
