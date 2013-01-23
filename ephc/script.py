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
    
    
# it was a good idea but it's busted because not all the config sections are the same
# arghhhhhhh    
#def do_healthcheck(section, check_class, **kwargs):
#    for item in section:
#        endpoint = section[item]['endpoint']
#        print item
#        hc = check_class(endpoint, **kwargs)
#        if hc.do_check():
#            print "{0:>80}".format('OK')
#        else:
#            message = "{0}{1}".format('FAILED: ', hc.message)
#            print "{0:>80}".format(message)
    

def check_endpoint(endpoint, check_class, **kwargs):
    
    # pass kwargs straight through, which can be stuff like db creds,
    # auth api user, key, and tenant id, etc....

    start_time = time()
    hc = check_class(endpoint, **kwargs)
    hc_ok = hc.do_check()
    end_time = time()
    lap_time = end_time - start_time
    
    return (hc_ok, hc.message, lap_time)

    
def check_all(config_chunk, check_class, **kwargs):
    for section in config_chunk:
        endpoint = config_chunk[section]['endpoint']
        # ... formulate kwargs to send
        result = check_endpoint(endpoint, check_class, **kwargs)
        print section, result


def run():
    # generic apis
    check_all(config['generic_api'], healthchecks.genericapi.GenericAPIHC)    
    
    # mysql
    check_all(config['databases']['mysql'], healthchecks.relationaldbs.MysqlHC,
              user=config['databases']['mysql'][mysqldb]['username'], 
              db=config['databases']['mysql'][mysqldb]['database'],
              passwd=config['databases']['mysql'][mysqldb]['password'], 
              query=config['databases']['mysql'][mysqldb]['query']
             )
              
    
    
def run2():
    options = get_arguments()
    
    results = {}
    
    # generic apis
    for gapi in config['generic_api']:
        gapi_endpoint = config['generic_api'][gapi]['endpoint']
        gapi_result = check_endpoint(gapi_endpoint, healthchecks.genericapi.GenericAPIHC)
        print gapi, gapi_result
        #if hc:
        #    results.update({'gapi': { 'status': 'OK', 'message': '', 'elapsed': lap_time}})
    
    # memcached
    for mc_cluster in config['memcached']:
        endpoint = config['memcached'][mc_cluster]['endpoint']
        mc_result = check_endpoint(endpoint, healthchecks.memcached.MemcacheHC)
        print mc_cluster, mc_result
    
    # mysql
    for mysqldb in config['databases']['mysql']:
        endpoint = config['databases']['mysql'][mysqldb]['endpoint']
        params = { 'user': config['databases']['mysql'][mysqldb]['username'], 
                   'db': config['databases']['mysql'][mysqldb]['database'],
                   'passwd': config['databases']['mysql'][mysqldb]['password'], 
                   'query': config['databases']['mysql'][mysqldb]['query'] }
        mysqlhc_result = check_endpoint(endpoint, healthchecks.relationaldbs.MysqlHC, **params)
        print mysqldb, mysqlhc_result
        
    
    # postgres
    for pgsqldb in config['databases']['pgsql']:
        endpoint = config['databases']['pgsql'][pgsqldb]['endpoint']
        params = { 'user': config['databases']['pgsql'][pgsqldb]['username'], 
                   'db': config['databases']['pgsql'][pgsqldb]['database'],
                   'passwd': config['databases']['pgsql'][pgsqldb]['password'], 
                   'query': config['databases']['pgsql'][pgsqldb]['query'] }
        pgsqlhc_result = check_endpoint(endpoint, healthchecks.relationaldbs.PgsqlHC, **params)
        print pgsqldb, pgsqlhc_result
        
    
    
def run_old():
    options = get_arguments()
    
    # let's do some temporary runs to make sure it works
    for gapi in config['generic_api']:
        endpoint = config['generic_api'][gapi]['endpoint']
        print gapi
        hc = healthchecks.genericapi.GenericAPIHC(endpoint)
        if hc.check_status() is True:
            print "{0:>80}".format('OK')
        else:
            # not sure how to align it all without doing this
            message = "{0}{1}".format('FAILED: ', hc.message)
            print "{0:>80}".format(message)
        
    # now memcached
    for group in config['memcached']:
        cluster = config['memcached'][group]
        print group
        mc = healthchecks.memcached.MemcacheHC(cluster)
        if mc.check_memcache() is True:
            print "{0:>80}".format('OK')
        else:
            message = "{0}{1}".format('FAILED: ', mc.message)
            print "{0:>80}".format(message)
            
    # now databases
    for pgsqldb in config['databases']['pgsql']:
        print pgsqldb
        shorthand = config['databases']['pgsql'][pgsqldb]
        params = { 'host': shorthand['endpoint'],
                   'user': shorthand['username'],
                   'passwd': shorthand['password'],
                   'db': shorthand['database'] }
        pigsqueal = healthchecks.relationaldbs.PgsqlHC(**params)
        if pigsqueal.check_pgsql() is True:
            print "{0:>80}".format('OK')
        else:
            message = "{0}{1}".format('FAILED: ', pigsqueal.message)
            print "{0:>80}".format(message)
            
    for mysqldb in config['databases']['mysql']:
        print mysqldb
        shorthand = config['databases']['mysql'][mysqldb]
        params = { 'host': shorthand['endpoint'],
                   'user': shorthand['username'],
                   'passwd': shorthand['password'],
                   'db': shorthand['database'] }
        mysqueal = healthchecks.relationaldbs.MysqlHC(**params)
        if mysqueal.check_mysql() is True:
            print "{0:>80}".format('OK')
        else:
            message = "{0}{1}".format('FAILED: ', mysqueal.message)
            print "{0:>80}".format(message)