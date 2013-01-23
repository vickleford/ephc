import optparse
from time import time

import healthchecks.genericapi
import healthchecks.memcached
import healthchecks.relationaldbs
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
    
    
def check_endpoint(endpoint, check_class, **kwargs):
    '''Return a tuple of info about the endpoint checked.
    
    endpoint is the value as it appears in config.yaml
    check_class is the name of the class as appears in local namespace
        from the healthchecks package
    kwargs' key will match additional parameters to a section of config, 
        such as a database username or a password. This will generally
        be built by check_all()
    '''
    
    start_time = time()
    hc = check_class(endpoint, **kwargs)
    hc_ok = hc.do_check()
    end_time = time()
    lap_time = end_time - start_time
    
    return (hc_ok, hc.message, lap_time)

    
def check_all(config_chunk, check_class, *args):
    '''Pass a section of config to check with check_endpoint.
    
    args should be any items in the config section additional
    to endpoint.
    '''
    
    for section in config_chunk:
        endpoint = config_chunk[section]['endpoint']
        
        # ... build kwargs to send to check_endpoint from args
        params = {}
        for arg in args:
            params.update({arg: config_chunk[section][arg]})
        
        result = check_endpoint(endpoint, check_class, **params)
        print section, result


def run():
    # generic apis
    check_all(config['generic_api'], healthchecks.genericapi.GenericAPIHC)    
    
    # mysql
    check_all(config['databases']['mysql'], healthchecks.relationaldbs.MysqlHC,
              'username', 'database', 'password', 'query')
              
    # pgsql
    check_all(config['databases']['pgsql'], healthchecks.relationaldbs.PgsqlHC,
             'username', 'database', 'password', 'query')
             
    # memcached
    check_all(config['memcached'], healthchecks.memcached.MemcacheHC)