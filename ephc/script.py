import os
import optparse
from time import time

import healthchecks.genericapi
import healthchecks.memcached
import healthchecks.relationaldbs
import healthchecks.relationaldbs

import formatters.stdout
import formatters.json_formatter
import formatters.bashmon

from config import config

# this will move to an argument later
verbose = False

def get_console_size():
    rows, columns = os.popen('stty size', 'r').read().split()
    
    return (rows, columns)


def get_arguments():
    parser = optparse.OptionParser()
    parser.add_option("-t", "--timeout", dest="timeout",
                      help="Time in seconds to time out a connection")
    #parser.add_option("-o", "--output", dest="output_type",
                      #help="help message", metavar="OPTION")
    #parser.add_option("-q", "--quiet",
                      #action="store_false", dest="verbose", default=True,
                      #help="dont print blah blah")
                      
    (options, args) = parser.parse_args()
    
    return options
    
    
def check_endpoint(endpoint, check_class, **kwargs):
    '''Return a tuple of info about the endpoint checked.
    
    Arguments:
    endpoint is the value as it appears in config.yaml
    check_class is the name of the class as appears in local namespace
        from the healthchecks package
    kwargs' key will match additional parameters to a section of config, 
        such as a database username or a password. This will generally
        be built by check_all()
        
    Return values:
    hc_ok is a boolean representing whether the endpoint passed or failed
    hc.message is a description of why the check failed or empty if it passed
    lap_time is the round trip time representing how long the check took
    '''
    
    if verbose:
        print "Checking {ep}...".format(ep=endpoint),
        
    start_time = time()
    hc = check_class(endpoint, **kwargs)
    hc_ok = hc.do_check()
    end_time = time()
    lap_time = round(end_time - start_time, 2)
    
    if verbose:
        if hc_ok:
            print "\n{0:>{1}}".format("[ PASSED ]", get_console_size()[1])
        else:
            print hc.message
            print "{0:>{1}}".format("[ FAILED ]", get_console_size()[1])
        print
    
    return (hc_ok, str(hc.message), lap_time)

    
def check_all(config_chunk, check_class, *args):
    '''Pass a section of config to check with check_endpoint.
    Health checks all entities in that chunk of config.
    
    args should be any items in the config section additional
    to endpoint.
    '''
    
    summary = {}
    
    for section in config_chunk:
        results = {}
        try:
            endpoint = config_chunk[section]['endpoint']
        except KeyError:
            endpoint = config_chunk[section]['endpoints']
        
        # ... build kwargs to send to check_endpoint from args
        params = {}
        for arg in args:
            params.update({arg: config_chunk[section][arg]})
        
        results['Success'], results['Reason'], results['Elapsed'] = \
            check_endpoint(endpoint, check_class, **params)
        results['Endpoint'] = endpoint
        summary.update({section: results})
        
    return summary
        
        
def aggregator(**kwargs):
    """Placeholder for an idea. Right now check_all gives back 1 dict per
    chunk of config you ask for. This will, if needed, aggregate all those
    dicts with section names.
    """
    
    aggregated_results = {}
    for report in kwargs:
        aggregated_results.update({report: kwargs[report]})
        
    return aggregated_results
    


def run():
    # generic apis
    genapi_results = check_all(config['generic_api'], 
                               healthchecks.genericapi.GenericAPIHC)    
    
    # mysql
    mysql_results = check_all(config['databases']['mysql'], 
                              healthchecks.relationaldbs.MysqlHC,
                              'username', 'database', 'password', 'query')
              
    # pgsql
    pgsql_results = check_all(config['databases']['pgsql'], 
                              healthchecks.relationaldbs.PgsqlHC,
                              'username', 'database', 'password', 'query')
             
    # memcached
    memcached_results = check_all(config['memcached'], 
                                  healthchecks.memcached.MemcacheHC)
                                  
    grand_summary = aggregator(generic_api=genapi_results, mysql=mysql_results,
                               pgsql=pgsql_results, memcached=memcached_results)
                               
    #formatter = formatters.stdout.StdoutFormatter(grand_summary)
    #formatter.format()
    
    #jsonformatter = formatters.json_formatter.JsonFormatter(grand_summary)
    #print jsonformatter.format()
    
    formatter = formatters.bashmon.BashMon(grand_summary)
    formatter.format()