from novella.logger.logger import logger
from novella.config.config import my_config
from novella.device.lampbody import Lampbody
from novella.device.lampshade import Lampshade
from novella.device.lamp import Lamp
from novella.database.database_client import my_database
from novella.filemanager.filemanger import my_filemanager
from novella.mqtt.mqtt_client import my_mqtt
from novella.response.response import my_responses
from novella.imageConverter import my_imageConverter

import flask
from flask import request, jsonify

app = flask.Flask(__name__)
api = config["DEBUG"] = True

class ApiLogger:
    @staticmethod
    def debug(*args):
        logger.debug("API", *args)

    @staticmethod
    def error(*args):
        logger.debug("API", *args)


# lamps endpoint
@app.route('/lamps', methods=['GET'])
def api_lamps():
    params = request.args

    command = params.get("command")     # Get command to be run


    ####
    # SET SETTING
    # args: command, device_type, lamp_name, setting, value
    ###
    if command == "set_setting":
        type = params.get("device_type")
        lampname = params.get("lamp_name")
        setting = params.get("setting")
        value = params.get("value")

        response = None
        try:
            tlamp = Lamp(name=lampname)
            if type="lampbody":
                tlamp.lampbody.set_setting(setting, value)
            if type="lampshade":
                tlamp.lamshade.set_setting(setting, value)
        except Exception as e:
            ApiLogger.debug(e)
            response = "error"
        else:
            response = "ok"

        return jsonify(response=response)


    ####
    # GET SETTING
    # args: command, lamp_name, device_type, setting
    ###
    if command == "get_setting":
        lampname = params.get("lamp_name")
        device_type = params.get("device_type")
        setting = params.get("setting")

        ans = None
        try:
            tlamp = Lamp(name=lampname)
            if type = "lampbody":
                ans = tlamp.lampbody.get_setting(setting)
            else if type = "lampshade":
                ans = tlamp.lampshade.get_setting(setting)
        except Exception as e:
            ApiLogger.debug(e)
            return jsonify(response="error")
        else:
            return jsonify(response="ok")


    ####
    # SEND IMAGE TO LAMP
    # args: command, lamp_name, image_name
    ###
    if command == "send_image":
        pass



    ####
    # SEND COMMAND TO LAMP
    # args: command, lamp_name, device_type, lamp_command
    ###
    if command == "send_command":
        lampname = params.get("lamp_name")
        type = params.get("device_type")
        lcommand = params.get("lamp_command")

        ans = None
        try:
            tlamp = Lamp(name=lampname)
            if type == "lampbody":
                ans = tlamp.lambody.send_command(lcommand)
            if type == "lampshade":
                ans = tlamp.lampshade.send_command(lcommand)
        except Exception as e:
            ApiLogger.debug(e)
            return jsonify(response="error")

        return jsonify(response = ans)

    ####
    # GET ONLINE DEVICES
    # args: command, device_type
    ###
    if command = "get_online_devices":
        type = params.get("device_type")
        ans = my_responses.get_online_devices(type)
        return jsonify(response=ans)


    ####
    # GET ONLINE LAMPS
    # args: command
    ###
    if command == "get_online_lamps":
        ans = my_responses.get_online_lamps()
        return jsonify(response=ans)


    ####
    # MAKE NEW LAMP
    # args: command, body_id, shade_id, lamp_name
    ###
    if command == "make_lamp":
        body_id = params.get("body_id")
        shade_id = params.get("shade_id")
        lampname = params.get("lamp_name")

        try:
            body = Lampbody(device_id=body_id)
            shade = Lampshade(device_id=shade_id)
            lamp = Lamp(name=lampname, lampbody=body, lampshade=shade)
        except Exception as e:
            ApiLogger.debug(e)
            jsonify(response="Error")
            return
        return jsonify(response="True")



if __name__ == '__main__':
    app.run(debug=True)
