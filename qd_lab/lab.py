import glob
from operator import truediv
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
from thermocontroller import thermocontroller
from thermocontroller.thermocontroller import Furnace
import threading
from pumps import milligat
from pumps import chemyx
from pumps.chemyx import *

thermo=Furnace()

# Shared dropbox folder
file_path = 'C:\\Users\\kvriz\\Desktop\\Leeds\\scripts\\test_folder\\' 

def printit():
  threading.Timer(5.0, printit).start()
  temp = read_temperature()
  with open("temperature_log.txt", "a") as file_object:
        file_object.write(str(datetime.now()) + ' ' + str(temp))
        file_object.write('\n')

def set_temperature(temperature):
    #thermo=Furnace()
    #thermo.connect()
    thermo.setpoint_1(temperature)

def read_temperature():
    #thermo=Furnace()
    return thermo.indicated()

def start_experiment(chemyx_rate, pump_rate_A=None, pump_rate_B=None, pump_rate_C=None, temperature=None, sampling_time):
    #"""Pump rate in mL min-1"""

    pump_a = milligat.Milligat('C', serial.Serial('COM10', 9600))
    pump_b = milligat.Milligat('C', serial.Serial('COM16', 9600))
    pump_c = milligat.Milligat('C', serial.Serial('COM8', 9600))

    chemyx_pump = chemyx.Connection('COM4', baudrate=9600, x = 0, mode = 0, verbose=False)
    chemyx_pump.openConnection()
    chemyx_pump.startPump()
    chemyx_pump.setUnits('mL/min')
    chemyx_pump.setRate(chemyx_rate)
            
    set_temperature(temperature)
    pump_a.set_flow_rate(pump_rate_A)
    pump_b.set_flow_rate(pump_rate_B)
    pump_c.set_flow_rate(pump_rate_C)
    time.sleep(sampling_time)

    # get the measurements from the analytical equipment
    # call the save spectra functions
    # Call the get responses function

    pump_a.stop_pump()
    pump_b.stop_pump()
    pump_c.stop_pump()
    chemyx_pump.stopPump()
    chemyx_pump.closeConnection()

# Command to run a single experiment with given settings
#start_experiment(pump_rate_A=None, pump_rate_B=None, pump_rate_C=25000, temperature=None) # mL min-1


#experiment_counter = 0

# Start recording the temperature
#printit()

#while True:
#    experiment_counter += 1    
#    while not os.path.exists(f'{file_path}\\{experiment_counter}_params.csv'):
#        time.sleep(5)             
    
#    params_dataset = pd.read_csv(f'{file_path}\\{experiment_counter}_params.csv')
#    pump_rate_A = params_dataset.pump_rate_A.values[0]
#    pump_rate_B = params_dataset.pump_rate_B.values[0]
#    pump_rate_C = params_dataset.pump_rate_C.values[0]
#    temperature = int(params_dataset.temperature.values[0])
    
#    start_experiment(pump_rate_A=pump_rate_A, pump_rate_B=pump_rate_B, pump_rate_C=pump_rate_C, temperature=temperature)
    
#    response_dataset = response_generator(params_dataset)
#    response_dataset.to_csv(f'{file_path}\\{experiment_counter}_response.csv', index=None)

#    if experiment_counter >= 3:
#        print('Process finished after 3 iterations!')
#        try:
#            stop_milligat_A()
#            stop_milligat_B()
#            stop_milligat_C()
#        except:
#            break


