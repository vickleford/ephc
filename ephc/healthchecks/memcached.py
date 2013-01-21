import uuid
import time

import memcache


class MemcacheHC(object):

    def __init__(self, memcache_servers):
        self.message = None
        self.mc = memcache.Client(memcache_servers, debug=0)

    def _set_key(self, key, value):
        '''Set a key in  memcache.'''
        
        success = self.mc.set(key, value)
        if success:
            return True
        else:
            self.message = "Could not set a key"
            return False
        
    def _read_key(self, key):
        '''Get the value of a key in memcache.'''
        
        return self.mc.get(key)
        
    def _delete_key(self, key):
        '''Unset a key in memcache.'''
        
        success = self.mc.delete(key)
        if success == 1:
            return True
        else:
            self.message = "Could not delete key"
            return False
        
    def check_memcache(self):
        '''Return True or False if memcache passes a health check.'''
        
        # gives us a safe uuid key name to avoid collisions 
        test_key = str(uuid.uuid4())
        test_value = time.time()
        
        # set a key
        set_ok = _set_key(test_key, test_value)

        # read the key
        if _read_key(test_key) == test_value:
            read_ok = True
        else:
            read_ok = False
            
        # delete the key
        delete_ok = _delete_key(test_key)
        
        # was it really deleted? 
        if _read_key(test_key) == None:
            delete_ok = True
        else:
            delete_ok = False
        
        # final check
        if and set_ok and read_ok and delete_ok:
            return True
        else:
            return False
            
        
        
    
#
# let's keep this around for now and delete later
#    
def _check_memcache_old_style(memcache_servers):
    '''Return a tuple after connecting to memcached, setting and deleting a key.'''

    try:
        mc = memcache.Client(memcache_servers, debug=0)

        test_value = time.time()
        # make a much safer key name than this
        set_success = mc.set("health_check", test_value)
        if set_success is not True:
            #print "Could not set a key!"
            #return False
            message = "Could not set a key"
            return (False, message)
        
        get_success = mc.get("health_check")
        if get_success != test_value:
            #print "Got a value for key that was not what we set!"
            #return False
            message = "Got a value for key that was not what we set"
            return (False, message)
        
        delete_success = mc.delete("health_check")
        if delete_success != 1:
            #print "Could not delete test key!"
            #return False
            message = "Could not delete test key"
            return (False, message)

        return (True, '')
    
    except Exception, e:
        #print "Memcached check failed: %s" % e
        #return False
        message = "Memcached check failed: %s" % e
        return (False, message)

    finally:
        mc.disconnect_all()