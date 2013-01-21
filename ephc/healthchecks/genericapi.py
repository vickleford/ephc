import urllib2


class GenericAPIHC(object):
    
    def __init__(self, url, timeout=5, fail_status=500, match=None):
        
        self.message = None
        self.conn = None
        
    def connect(self, url, timeout=5, fail_status=500):
        try:
            self.conn = None
            self.conn = urllib2.urlopen(url, timeout=timeout)
        except ValueError, e:
            self.message = e.message
        except urllib2.HTTPError, e:
            if e.code < fail_status:
                e.message = "Got response %d, but with error: %s" % (e.code, e.reason)
            else:
                self.message = e
        except urllib2.URLError, e:
            self.message = e
        finally:
            if conn:
                conn.close()
    
    def match_content(self, match=None):
        content = self.conn.read()
        if match in content:
            return True
        else:
            return False
    
    
    

#
# let's keep this around for now and delete later
#    

def _check_api(url, timeout=5, fail_status=500):
    "Return True if a HTTP status code is less than fail_status."

    try:
        conn = None
        conn = urllib2.urlopen(url, timeout=timeout)
    except urllib2.HTTPError, e:
        if e.code < fail_status:
            print "Got a response (%d), but with error: %s" % (e.code, e.reason)
            return True
        else:
            print "%s" % e
    except urllib2.URLError, e:
        print "%s" % e
    else:
        # prevents OK messages from going out on the same line
        print
    finally:
        if conn:
            conn.close()
    
    if conn is not None and conn.code < fail_status:
        return True
    else:
        return False