import optparse

import healthchecks.genericapi
import healthchecks.memcached
import healthchecks.relationaldbs

from config import config


def get_arguments():
    parser = optparse.OptionParser()
    #parser.add_option("-o", "--output", dest="output_type",
                      #help="help message", metavar="OPTION")
    #parser.add_option("-q", "--quiet",
                      #action="store_false", dest="verbose", default=True,
                      #help="dont print blah blah")
                      
    (options, args) = parser.parse_args()
    
    return options
    
def run():
    options = get_arguments()
    
    # let's do some temporary runs to make sure it works
    for gapi in config['generic_api']:
        endpoint = config['generic_api'][gapi]['endpoint']
        print gapi, endpoint
        hc = healthchecks.genericapi.GenericAPIHC(endpoint)