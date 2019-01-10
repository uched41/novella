from novella.database.database_client import my_database
import time


# This class object will store the response from each device

class Response:
    def __init__(self):
        self.data = dict()

    # self.data = {
    #           "D91980029":{
    #               "response":"OK",
    #               "type     : "lampbody",
    #               "new"     : True,
    #               "last_updated"  : 499,
    #               },
    #       }
    def set(self, type, device, response):       # set a response value
        self.data[device]["type"] = type
        self.data[device]["response"] = response
        self.data[device]["new"] = True
        self.data[device]["last_updated"] = time.time()


    def get(self, device, val):         # Get response value
        tdata = self.data.get(device)
        if tdata and val in tdata.keys():
            self.data[device]["new"] = False
            return self.data[device][val]
        return None


    def set_online(self, device):
        self.data[device]["last_updated"] = time.time()


    def is_online(self, device):
        dev = self.data.get(device):
        if time.time() - dev.get("last_updated") < (60*5):
            return True
        return False


    def get_online_devices(self, type):     # get devices of a particular type that are online
        ans = []
        for dev in self.data.keys():
            dev = self.data.get(dev)
            if dev.get("type") == type:
                if ( time.time() - dev.get("last_updated") < (60*5) ):   # check timeout of 5mins
                    ans.append(dev)


    def get_online_lamps(self):
        ans = self.get_online_devices(self, "lampbody"):
        tans = []
        # get names of lamps whose lampbodies are online
        for body in ans:
            temp = my_database.get_from_table(table="lamps", column="lambody_id",\
                    query=body, dcolumn=["name"])
            temp = temp[0][0]
            tans.append(temp)

        return tans


    def wait_reply(self, device, timeout=3):
        oldTime = time.time()
        while (time.time()-oldTime < (timeout*60) ):
            if self.data[device]["new"] is True:
                res = self.data[device]["response"]
                return res
        return None


# response instance
my_responses = Response()
