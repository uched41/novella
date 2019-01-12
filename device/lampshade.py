from novella.logger.logger import logger
from novella.database.database_client import my_database
from novella.config.config import my_config
from novella.device.mcu import Mcu
from novella.response.response import my_responses
from novella.image.imageConverter import my_imageConverter
from novella.filemanager.filemanager import my_filemanager
import os, math

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


    def send_image(imgname):
        if my_imageConverter.convert_image(imgname) is False:
            return "error"

        BUF_SIZE = 1024
        bin_name = imgname.split('.')[0] + ".bin"
        topic = "novella/devices/{}/{}/".format(self.device_id, "bin-data")

        # to start we add 'start' to end of topic and send
        # device will read this topic end and act accordingly
        ntopic = topic + "start"
        fpath = os.path.join(my_filemanager.bin_dir, bin_name)
        no_lines = os.stat(fpath).st_size / BUF_SIZE
        no_lines = math.ceil(no_lines)

        ndata = { "filename": bin_name, "no_lines": no_lines}

        my_mqtt.publish(ntopic, str(ndata))

        atopic = topic + "mid"

        with open(fpath, 'rb') as myfile:
            temp = True
            while temp:
                temp = myfile.read(1024)
                my_mqtt.publish(atopic ,temp)
                my_responses.wait_reply(self.device.id) # wait for reply from device

        ltopic = topic + "end"
        my_mqtt.publish(ltopic, "End")


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


#my_lampshade = Lampshade(device_id="D89340332")
