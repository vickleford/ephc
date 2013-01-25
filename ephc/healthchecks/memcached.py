import uuid
import time

import memcache


class MemcacheHC(object):

    def __init__(self, memcache_servers, **kwargs):
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
        set_ok = self._set_key(test_key, test_value)

        # read the key
        if self._read_key(test_key) == test_value:
            read_ok = True
        else:
            read_ok = False
            
        # delete the key
        delete_ok = self._delete_key(test_key)
        
        # was it really deleted? 
        if self._read_key(test_key) == None:
            delete_ok = True
        else:
            delete_ok = False
        
        # final check
        if set_ok and read_ok and delete_ok:
            return True
        else:
            return False
            
    def do_check(self):
        return self.check_memcache()
