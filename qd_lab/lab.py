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


pump_c = milligat.Milligat('C', serial.Serial('COM8', 9600))
pump_c.set_flow_rate(1000)
pump_c.stop_pump()

def printit():
  threading.Timer(5.0, printit).start()
  temp = read_temperature()
  with open("temperature_log.txt", "a") as file_object:
        file_object.write(str(datetime.now()) + ' ' + str(temp))
        file_object.write('\n')

# Milligat serial channels
ser8 = serial.Serial('COM8',9600) # pump C
ser10 = serial.Serial('COM10',9600) # pump A
ser16 = serial.Serial('COM16',9600) # pump B
thermo=Furnace()

# Shared dropbox folder
file_path = 'C:\\Users\\kvriz\\Desktop\\Leeds\\scripts\\test_folder\\' 

def getResponse(ser):
    try:
        response_list = []
        while True:
            response = ser.readlines()
            for line in response:
                line = line.strip(b'\n').decode('utf8')
                line = line.strip('\r')
                response_list.append(line)
            break
        return response_list
    except:
            ser.close()

def set_temperature(temperature):
    #thermo=Furnace()
    #thermo.connect()
    thermo.setpoint_1(temperature)

def read_temperature():
    #thermo=Furnace()
    return thermo.indicated()

def start_pump_A(pump_rate): 
    """Pump rate is given in mL min-1 and is then adjusted according 
    to the Milligat rate"""
    #milligat_rate = pump_rate*13397.87686
    try:
        ser10.open()
    except:pass
    msg=f'ASL = {pump_rate}\r\n'.encode()
    ser10.write(msg)
    #getResponse(ser10)

def stop_milligat_A():
    msg=f'ASL = 0\r\n'.encode()
    ser10.write(msg)
    ser10.close()
    print('Pumping from pump A has finished')

def start_pump_B(pump_rate): 
    """Pump rate is given in mL min-1 and is then adjusted according 
    to the Milligat rate"""
    #milligat_rate = pump_rate*13397.87686
    try:
        ser11.open()
    except:pass
    msg=f'BSL = {pump_rate}\r\n'.encode()
    ser11.write(msg)
    #getResponse(ser11)

def stop_milligat_B():
    msg=f'BSL = 0\r\n'.encode()
    ser11.write(msg)
    ser11.close()
    print('Pumping from pump B has finished')

def start_pump_C(pump_rate): 
    """Pump rate is given in mL min-1 and is then adjusted according 
    to the Milligat rate"""
    #milligat_rate = pump_rate*13397.87686
    try:
        ser8.open()
    except:pass
    msg=f'CSL = {pump_rate}\r\n'.encode()
    ser8.write(msg)
    #getResponse(ser8)

def stop_milligat_C():
    msg=f'CSL = 0\r\n'.encode()
    ser8.write(msg)
    ser8.close()
    print('Pumping from pump C has finished')

def start_experiment(pump_rate_A=None, pump_rate_B=None, pump_rate_C=None, temperature=None):
    #"""Pump rate in mL min-1"""
    
    set_temperature(temperature)
    
    start_pump_A(pump_rate_A)
    start_pump_B(pump_rate_B)
    start_pump_C(pump_rate_C)
    time.sleep(60)
    stop_milligat_A()
    stop_milligat_B()
    stop_milligat_C()


# Command to run a single experiment with given settings
#start_experiment(pump_rate_A=None, pump_rate_B=None, pump_rate_C=25000, temperature=None) # mL min-1

# Read the params file and add the response
def response_generator(params_dataset):
    df = params_dataset 
    df['response'] = pd.DataFrame(np.random.rand(1,1),
                   columns=['conversion'])
    return df

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


