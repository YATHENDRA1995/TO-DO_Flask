import psycopg2
from configparser import ConfigParser
CONFIG_FILE = "config.conf"
config = ConfigParser()
config.read(CONFIG_FILE)


class MySqlClient(object):

    def __init__(self):
        self.host = None
        self.username = None
        self.password = None
        self.db_name = None
        self.db = None
        self.cur = None
        self.read_configurations()

    def read_configurations(self):
        try:
            self.host = config.get("dbsettings_local", "host")
            self.username = config.get("dbsettings_local", "username")
            self.password = config.get("dbsettings_local", "password")
            self.db_name = config.get("dbsettings_local", "db_name")
        except Exception as e:
            logger.error("Exception while Fetching Config Details: "+str(e))

    def connect(self):
        try:
            self.db = psycopg2.connect(database=self.db_name, port=5432, user=self.username,
                                       host=self.host, password=self.password)
            self.cur = self.db.cursor()
            return self.cur
        except Exception as e:
            print("exception while making connection ", e)
            logger.error(str(e))

    def execute_fetchall(self, query):
        try:
            cursor = self.connect()
            cursor.execute(query)
            result = cursor.fetchall()
            cursor.close()
            return result
        except Exception as e:
            logger.error("Exception while Fetching: "+str(e))
            return False

    # execute fetchone
    # def execute_fetchone(self, query):
    #     try:
    #         cursor = self.connect()
    #         cursor.execute(query)
    #         result = cursor.fetchone()
    #         cursor.close()
    #         return result
    #     except Exception as e:
    #         logger.error("Exception while Fetching: " + str(e))
    #         return False

    # update table
    def update_table(self, query, data=[]):
        try:
            cursor = self.connect()
            cursor.execute(query, data)
            self.db.commit()
            cursor.close()
            return True
        except Exception as e:
            print(e)
            logger.error("Exception while updating:  :"+str(e))
            return False

    # create table
    # def create(self, query):
    #     try:
    #         cursor = self.connect()
    #         cursor.execute(query)
    #         result = cursor.execute(query)
    #         # result = cursor.fetchall()
    #         cursor.close()
    #         return result
    #     except Exception as e:
    #         logger.error("Exception while Fetching: "+str(e))
    #         return False

    def close_connection(self):
        self.db.close()