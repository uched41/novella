from novella.logger.logger import logger
import MySQLdb as mysql
from novella.config.config import my_config

class Database:

    def __init__(self, mysql_host, mysql_user, mysql_password, mysql_db):

        self.__host = mysql_host
        self.__user = mysql_user
        self.__password = mysql_password
        self.__database = mysql_db



    def connect(self):

        Database.debug("Connecting to database")
        try:
            self.__mydb = mysql.connect(host=self.__host, user=self.__user, passwd=self.__password, db=self.__database)
        except Exception as e:
            Database.error("Error initializing database")
            return False
        else:
            return True


    def run_command(self, **kwargs):

        if not self.connect() or "command" not in kwargs.keys():   # connect to database first
            return False

        command = kwargs["command"]
        cursor = self.__mydb.cursor()

        try:
            # Check if we have to pass options
            if "params" not in kwargs.keys():
                cursor.execute(command)
            else:
                params = kwargs["params"]
                cursor.execute(command, params)
        except Exception as e:
            Database.error(e)
            return False

        self.__mydb.commit()

        result = cursor.fetchall()
        cursor.close()              # Close connection
        self.__mydb.close()
        return result


    def change_database(self, **kwargs):
        if "database" not in kwargs.keys():
            Database.error("Unable to change database")
            return None

        command = "USE {}".format(kwargs["database"])
        return self.run_command(command=command)


    def create_table(self, **kwargs):
        if not Database.in_list(["columns", "table"], kwargs.keys()):
            Database.error("Unable to create table")
            return None

        command = "CREATE TABLE IF NOT EXISTS {} {}".format(kwargs["table"], kwargs["columns"])
        return self.run_command(command=command)


    def is_in_table(self, **kwargs):
        if not Database.in_list(["table", "column", "query"], kwargs.keys()):
            raise Exception
            return False

        table = kwargs["table"]
        column = kwargs["column"]
        query = kwargs["query"]
        cmd = "SELECT * FROM {} where {} like '%{}%' ".format(table, column, query)

        ans = self.run_command(command=cmd)
        if len(ans) == 0:
            return False
        else:
            return True


    def insert_in_table(self, **kwargs):
        if not Database.in_list(["table", "template", "value"], kwargs.keys()):
            raise Exception
            return False

        table = kwargs["table"]
        template = kwargs["template"]
        value = kwargs["value"]
        cmd = "INSERT INTO {} {} ".format(table, template)
        return self.run_command(command=cmd, params=value)


    def get_from_table(self, **kwargs):
        if not Database.in_list( ["table", "column", "query"], kwargs.keys() ):
            raise Exception
            return False

        table = kwargs["table"]
        column = kwargs["column"]
        query = kwargs["query"]

        if "dcolumn" in kwargs.keys():      # if we want to select a particular column or columns
            dcolumn = kwargs["dcolumn"]

            if not isinstance(dcolumn, list):
                raise Exception("Dcolumn must be of type list")

            cmd = "SELECT "
            for col in dcolumn:
                cmd = cmd + col
                if dcolumn.index(col) == len(dcolumn)-1:
                    cmd = cmd + " "
                else:
                    cmd = cmd + ", "

            cmd = cmd + "FROM {} WHERE {}='{}'".format(table, column, query)
            return self.run_command(command=cmd)

        else:               # select all columns
            cmd = "SELECT * FROM {} WHERE {}='{}'".format(table, column, query)
            return self.run_command(command=cmd)


    def update_table(self, **kwargs):
        if not Database.in_list( ["table", "scolumns", "dcolumn", "dvalue", "value"], kwargs.keys() ):
            raise Exception
            return False

        table = kwargs["table"]
        scolumns = kwargs["scolumns"]   # columns to set
        dcolumn = kwargs["dcolumn"]   # column to query
        dvalue = kwargs["dvalue"]       # value to match
        value = kwargs["value"]

        if not isinstance(scolumns, list) or not isinstance(value, list):
            raise Exception("scolumns and value arguments must be of type list")
            return False
 
        cmd = "UPDATE {} SET ".format(table)
        for col in scolumns:
            cmd = cmd + col + " = %s"
            if scolumns.index(col) == len(scolumns)-1:
                cmd = cmd + " "
            else:
                cmd = cmd + ", "

        cmd = cmd + "WHERE {}='{}'".format(dcolumn, dvalue)
        return self.run_command(command=cmd, params=value)


    @staticmethod
    def in_list(items, dlist):         # Function to check if a items are in a list
        for item in items:
            if item not in dlist:
                return False

        return True


    @staticmethod
    def debug(*args):
        logger.debug("Database", *args)


    @staticmethod
    def error(*args):
        logger.error("Database", *args)



# Database object
mysql_host = my_config.get("database", "host")
mysql_user = my_config.get("database", "user")
mysql_password = my_config.get("database", "password")
mysql_database = my_config.get("database", "database")

my_database = Database(mysql_host, mysql_user, mysql_password, mysql_database)
