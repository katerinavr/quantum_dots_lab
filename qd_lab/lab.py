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

def start_experiment(chemyx_rate=None, pump_rate_A=None, pump_rate_B=None, pump_rate_C=None, temperature=None, sampling_time=None,
    com_A=None, com_B=None, com_C=None):
    #"""Pump rate in mL min-1"""
    if pump_rate_A != None:
        pump_a = milligat.Milligat('B', serial.Serial(com_A, 9600))
    if pump_rate_B != None:
        pump_b = milligat.Milligat('B', serial.Serial(com_B, 9600))
    if pump_rate_C != None:
        pump_c = milligat.Milligat('C', serial.Serial(com_C, 9600))

    if chemyx_rate != None:
        chemyx_pump = chemyx.Connection('COM4', baudrate=9600, x = 0, mode = 0, verbose=False)
        chemyx_pump.openConnection()
        chemyx_pump.startPump()
        chemyx_pump.setUnits('mL/min')
        chemyx_pump.setRate(chemyx_rate)

    if temperature != None:
        set_temperature(temperature)

    if pump_rate_A != None:
        pump_a.set_flow_rate(pump_rate_A)

    if pump_rate_B != None:
        pump_b.set_flow_rate(pump_rate_B)

    if pump_rate_C != None:
        pump_c.set_flow_rate(pump_rate_C)

    time.sleep(sampling_time*60)
    print('Stopping the pumps')
    # get the measurements from the analytical equipment
    # call the save spectra functions
    # Call the get responses function

    #if temperature != None:
    pump_a.set_flow_rate(0)
    #if pump_rate_B != None:
    pump_b.set_flow_rate(0)
    #if pump_rate_C != None:
    #    pump_c.set_flow_rate(0)
    #if chemyx_rate != None:
    #    chemyx_pump.stopPump()
    #    chemyx_pump.closeConnection()

# Command to run a single experiment with given settings
#start_experiment(pump_rate_A=None, pump_rate_B=None, pump_rate_C=25000, temperature=None) # mL min-1





