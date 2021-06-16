# Must imports
from slips.common.abstracts import Module
import multiprocessing
from slips.core.database import __database__
import platform

# Your imports
import time
import maxminddb
import ipaddress
import os, pwd

class Module(Module, multiprocessing.Process):
    name = 'geoip'
    description = 'Module to find the cCountry and geolocaiton information of an IP address'
    authors = ['Sebastian Garcia']

    def __init__(self, outputqueue, config):
        multiprocessing.Process.__init__(self)
        # All the printing output should be sent to the outputqueue. The outputqueue is connected to another process called OutputProcess
        self.outputqueue = outputqueue
        # In case you need to read the slips.conf configuration file for your own configurations
        self.config = config
        # Start the DB
        __database__.start(self.config)
        # Open the maminddb offline db
        try:
            self.reader = maxminddb.open_database('modules/geoip/GeoLite2-Country.mmdb')
        except:
            self.print('Error opening the geolite2 db in ./GeoLite2-Country_20190402/GeoLite2-Country.mmdb. Please download it from https://geolite.maxmind.com/download/geoip/database/GeoLite2-Country.tar.gz. Please note it must be the MaxMind DB version.')
        # To which channels do you wnat to subscribe? When a message arrives on the channel the module will wakeup
        self.c1 = __database__.subscribe('new_ip')
        # Set the timeout based on the platform. This is because the pyredis lib does not have officially recognized the timeout=None as it works in only macos and timeout=-1 as it only works in linux
        if platform.system() == 'Darwin':
            # macos
            self.timeout = None
        elif platform.system() == 'Linux':
            self.timeout = None
        else:
            #??
            self.timeout = None
        # If the module requires root to run, comment this
        self.drop_privileges()

    def drop_privileges(self):
        """ Remove root privileges if the process doesn't need them """

        if os.getuid() != 0:
            # your'e not root
            return
        # get the second user in user list , first one is root
        # we're looking for a user that isn't root
        try:
            userinfo = pwd.getpwall()[1]
            gid_name = userinfo[3]
            uid_name =  userinfo[2]
        except IndexError:
            return
        # Remove group privileges
        os.setgroups([])
        # Try setting the new uid/gid
        os.setgid(gid_name)
        os.setuid(uid_name)
        return

    def print(self, text, verbose=1, debug=0):
        """ 
        Function to use to print text using the outputqueue of slips.
        Slips then decides how, when and where to print this text by taking all the prcocesses into account

        Input
         verbose: is the minimum verbosity level required for this text to be printed
         debug: is the minimum debugging level required for this text to be printed
         text: text to print. Can include format like 'Test {}'.format('here')
        
        If not specified, the minimum verbosity level required is 1, and the minimum debugging level is 0
        """

        vd_text = str(int(verbose) * 10 + int(debug))
        self.outputqueue.put(vd_text + '|' + self.name + '|[' + self.name + '] ' + str(text))

    def run(self):
        try:
            # Main loop function
            while True:
                message = self.c1.get_message(timeout=self.timeout)
                # if timewindows are not updated for a long time, Slips is stopped automatically.
                if message['data'] == 'stop_process':
                    return True
                elif message['channel'] == 'new_ip':
                    ip = message['data']
                    # The first message comes with data=1
                    if type(ip) == str:
                        data = __database__.getIPData(ip)
                        ip_addr = ipaddress.ip_address(ip)

                        # Check that there is data in the DB, and that the data is not empty, and that our key is not there yet
                        if (not data or 'geocountry' not in data) and not ip_addr.is_multicast:
                            geoinfo = self.reader.get(ip)
                            if geoinfo:
                                try:
                                    countrydata = geoinfo['country']
                                    countryname = countrydata['names']['en']
                                    data = {}
                                    data['geocountry'] = countryname
                                except KeyError:
                                    data = {}
                                    data['geocountry'] = 'Unknown'
                            elif ipaddress.ip_address(ip).is_private:
                                # Try to find if it is a local/private IP
                                data = {}
                                data['geocountry'] = 'Private'
                            else:
                                data = {}
                                data['geocountry'] = 'Unknown'
                            __database__.setInfoForIPs(ip, data)


        except KeyboardInterrupt:
            if self.reader:
                self.reader.close()
            return True
        except Exception as inst:
            if self.reader:
                self.reader.close()
            self.print('Problem on the run()', 0, 1)
            self.print(str(type(inst)), 0, 1)
            self.print(str(inst.args), 0, 1)
            self.print(str(inst), 0, 1)
            return True
