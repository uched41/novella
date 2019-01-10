from novella.logger.logger import logger
from novella.database.database_client import my_database
from novella.config.config import my_config
from novella.mcu.mcu import Mcu

lampshade_columns = " (No INT AUTO_INCREMENT, device_id TEXT, current_pair TEXT, settings TEXT, misc TEXT, PRIMARY KEY (No) ) "


# Lampshade class which inherites parent class Mcu
class Lampshade(Mcu):

    def __init__(self, **kwargs):
        # create table if it doesnt exist already
        if my_database.create_table(table="lampshades", columns=lampshade_columns) is False:
            raise Exception("Unable to create table - lampshades")

        self.device_id = kwargs["device_id"]
        self.group = "lampshades"            # to be used by parent class to access Database Table

        # check if device already in database or not
        if not my_database.is_in_table(table="lampshades", column="device_id", query=self.device_id):

            # create entry for new lampshade
            table = "lampshades"
            template = " (device_id, settings) VALUES (%s, %s) "
            self.settings = my_config.get("lampshade", "default_settings")
            values = [self.device_id, str(self.settings)]

            if my_database.insert_in_table(table=table, template=template, value=values) is False:
                raise Exception("Unable to create lampshade object")

            Lampshade.debug("Created new lampshade object: " + self.device_id)

        else:       # is the device is already in our database
            Lampshade.debug("Device already in database: " + self.device_id)



    def __str__(self):
        return self.device_id


    @staticmethod
    def debug(*args):
        global logger
        logger.debug("Lampshade", *args)


    @staticmethod
    def error(*args):
        global logger
        logger.error("Lampshade", *args)


my_lampshade = Lampshade(device_id="D89340332")
