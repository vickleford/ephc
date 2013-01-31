import urllib2
import socket


class GenericAPIHC(object):
    
    def __init__(self, url, timeout=5, fail_status=500, **kwargs):
        
        self.message = None
        self.url = url
        self.timeout = timeout
        self.fail_status = fail_status
        self.got_code = None
        self.match = kwargs['match']
        self.conn = None
        self.content = None
        
    def connect(self):
        try:
            self.conn = urllib2.urlopen(self.url, timeout=self.timeout)
            self.got_code = self.conn.code
            self.content = self.conn.read()
        except ValueError, e:
            self.message = e.message
        except urllib2.HTTPError, e:
            if e.code <= self.fail_status:
                self.message = "Got a response, but with error: %d: %s" % (e.code, e.reason)
                self.got_code = e.code
            else:
                self.message = e
        except urllib2.URLError, e:
            self.message = e
        except socket.timeout, e:
            self.message = e
                
    def disconnect(self):
        if self.conn is not None:
            self.conn.close()
    
    def check_status(self):
        #self.connect()
        
        try:
            if self.got_code <= self.fail_status:
                ok = True
            else:
                ok = False
        except AttributeError:
            # there was no connection
            return False
        
        return ok
        
    def match_content(self):
        
        try:
            if self.match in self.content:
                return True
            else:
                return False
        except TypeError:
            # self.content is still none because we couldn't connect
            return False
                
    def do_check(self):
        #integrate check_status and match_content into one big ole package
        # watch out for the self.disconnect() in match_content and 
        # check_status! put those in a try...finally type thing later
        #something like this....
        self.connect()
        status_ok = self.check_status()
        content_ok = self.match_content()
        self.disconnect()
        
        return self.check_status() and content_ok