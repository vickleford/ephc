import urllib2


class GenericAPIHC(object):
    
    def __init__(self, url, timeout=5, fail_status=500, match=None, **kwargs):
        
        self.message = None
        self.url = url
        self.timeout = timeout
        self.fail_status=fail_status
        self.match=match
        self.conn = None
        
    def connect(self):
        try:
            self.conn = urllib2.urlopen(self.url, timeout=self.timeout)
        except ValueError, e:
            self.message = e.message
        except urllib2.HTTPError, e:
            if e.code < self.fail_status:
                self.message = "Got a response, but with error: %d: %s" % (e.code, e.reason)
            else:
                self.message = e
        except urllib2.URLError, e:
            self.message = e
                
    def disconnect(self):
        if self.conn is not None:
            self.conn.close()
    
    def check_status(self):
        self.connect()
        
        try:
            if self.conn.code < self.fail_status:
                ok = True
            else:
                ok = False
        except AttributeError:
            # there was no connection
            return False
        
        self.disconnect()
        return ok
        
    def match_content(self):
        connect()
        
        content = self.conn.read()
        if match in content:
            return True
        else:
            return False
        
        self.disconnect()
        
    def do_check(self):
        #integrate check_status and match_content into one big ole package
        # watch out for the self.disconnect() in match_content and 
        # check_status! put those in a try...finally type thing later
        #something like this....
        return self.check_status()