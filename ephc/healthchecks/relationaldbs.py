"""advised 2 separate classes here, 1 for each"""

import psycopg2
import MySQLdb
import _mysql_exceptions


class MysqlHC(object):
    
    def __init__(self, host, **kwargs):
        self.test_query = kwargs['query']
        self.message = None
        self.code = None
        self.params = { 'host': host,
                        'user': kwargs['username'],
                        'passwd': kwargs['password'],
                        'db': kwargs['database'] }
        
    def check_mysql(self):
        try:
            db_conn = None
            db_conn = MySQLdb.connect(**self.params)
            cur = db_conn.cursor()
            success = cur.execute(self.test_query)
            return True
        except _mysql_exceptions.OperationalError, e:
            self.code = e[0]
            self.message = e[1]
            return False
        except MySQLdb.Error, e:
            self.message = e
            return False
        finally:
            if db_conn is not None:
                db_conn.close()
                
    def do_check(self):
        return self.check_mysql()
                
                
class PgsqlHC(object):
    
    def __init__(self, host, **kwargs):
        self.test_query = kwargs['query']
        self.message = None
        self.code = None # is this used?
        
        # out of order to be consistent with connect_mysql args
        self.conn_str = "host='%s' dbname='%s' user='%s' password='%s'" % \
            (host, kwargs['database'], kwargs['username'], kwargs['password'])
        
    def check_pgsql(self):
        try:
            conn = None
            conn = psycopg2.connect(self.conn_str)
            cursor = conn.cursor()
            cursor.execute(self.test_query)
            records = cursor.fetchall()
            return True
        except Exception, e:
            self.message = e
            return False
        finally:
            if conn is not None:
                conn.close()
                
    def do_check(self):
        return self.check_pgsql()