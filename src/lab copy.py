import glob
import os
import time
from datetime import datetime, timedelta
import warnings
from collections import defaultdict
import json
import serial
import numpy as np
import pandas as pd
from pandas.api.types import is_numeric_dtype
import glob 
from core import thermocontroller
from core.thermocontroller import Furnace

class Laboratory():
    """This is some comment for the laboratory"""

    def __init__(self, project_name=None, debug=False):
        
        self.furnace = [None]
        # if project_name:
        #     self.load_data(os.path.join(config.DATA_DIR, project_name))
        # else:
        #     self.load_instruments() 
    
    def load_instruments(self):
        """Loads the laboratory instruments. Called automatically when calling Setup() without a filename specified.
        :returns: lcr, daq, gas, furnace, stage
        :rtype: instrument objects
        """
        self.furnace = Furnace.connect()

    def shutdown(self):
        """Returns the furnace to a safe temperature and closes ports to both the DAQ and LCR. (TODO need to close ports to stage and furnace)
        """
        self.furnace.shutdown()


class LabEquipment:

    def __init__(self, port, baudrate):
        self.port = port
        self.baudrate = baudrate

    def open(self):
        self.ser = serial.Serial()
        self.ser.baudrate = self.baudrate
        self.ser.port = self.port
        self.ser.open()
        if self.ser.isOpen():
            print('Port connection open')
    
    def close(self):
        self.ser.close()
        print("Closed connection")
    
    def send_msg(self, msg):
        arg = f'{msg}\r\n'.encode()
        #f'CSL = 0\r\n'.encode() 
        self.ser.write(arg)
        time.sleep(0.5)
        response = self.recv_msg()
        return response
            
    def recv_msg(self):
        response_list = []
        while True:
            response = self.ser.readlines()
            for line in response:
                line = line.strip(b'\n').decode('utf8')
                line = line.strip('\r')
                if self.verbose:
                    print(line)
                response_list.append(line)
            break
        return response_list
    
    def update_settings(self, config):
        """Updates the settings of the lab equipment.

        Should be implemented by certain subclasses."""
        pass

class MilliGatPump(LabEquipment):
    def __init__(self, port, baudrate):
        super().__init__(port, baudrate)
        #self.ser = serial.Serial()
    
    def start_pump(self, pump_rate):
        command = 'CSL = %s'%pump_rate
        response = self.send_msg(command)
        return response

    def stop_pump(self):
        command = 'CSL = 0'
        response = self.send_msg(command)
        return response

    def set_flow_rate(self, flow_rate, units):
        pass

    def update_settings(self, config):
        """Individual pumps don't need to implement this."""
        self.set_flow_rate(config['flowrate'], config['units'])

equip = {'milligat': MilliGatPump('COM4', 9600)
         }

while True:
    pump = MilliGatPump('COM4', 9600)
    pump.open()
    pump.start_pump(46200)
    time.sleep(30)
    # Fetch conditions
    #conditions = {'milligat': {'flowrate': 46200},
      #            }

   # for key, values in conditions.items():
     #   equip[key].update_settings(values)

    # Sleep for some time
    #time.sleep(30)