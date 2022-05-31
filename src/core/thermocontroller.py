"""
Contains the drivers for the Eurotherm 3216
Code inspired from https://github.com/SSJenny90/laboratory/
"""

import math
import os
import pickle
from functools import wraps
import numpy as np
from datetime import timedelta
import time


from serial.tools import list_ports
import minimalmodbus

#-------------------Eurotherm settings-------------------
FURNACE_ADDRESS = 'COM9'
RESET_TEMPERATURE = 20       #temperature the furnace resets to
#-------------------Eurotherm settings-------------------

class Furnace(minimalmodbus.Instrument):
    """Driver for the Eurotherm 3216 Temperature Controller
        .. note::
        units are in °C
        =============== ===========================================================
        Attributes      message
        =============== ===========================================================
        default_temp     revert to this temperature when resetting
        status           whether the instrument is connected
        address         computer port address
        =============== ===========================================================
        """

    default_temp = RESET_TEMPERATURE

    def __init__(self):
        self.port = FURNACE_ADDRESS
        self.target = self.default_temp
        try:
            super().__init__(self.port, 1)
        except Exception as e:
            print('Could not connect to the {}!'.format(self.__class__.__name__))
            
        else:
            print('{} connected at {}'.format(
                self.__class__.__name__, self.port))
            # self.close_port_after_each_call = True
            self.serial.baudrate = 9600
            # self.command(276,1) #set to remote setpoint
            self.status = True
            self.configure()

    def __str__(self):
        return '\n'.join([key+": "+str(val) for key, val in self.__dict__.items()])

    def configure(self):
        """Configures the furnace based on settings specified in the configuration file"""
        print('Configuring furnace...')
        # self.setpoint_2()
        self.setpoint_select('setpoint_1')
        self.display(0)
        self.timer_type('dwell')
        self.timer_end_type('current')
        self.timer_resolution('M:S')
        #self.timer_status('reset')

    def display(self, display_type=0, address=106):
        """
        Select the display mode for the furnace.
        options:
            0 : Standard PV and SP
            1 : PV and output power
            2 : PV and time remaining
            3 : PV and timer elapsed
            4 : PV and alarm 1 setpoint
            5 : PV and load current
            6 : PV only
            7 : PV and composite SP/time remaining
        :param display_type: any display type options as above
        :type display_type: int
        :returns: True if succesful, False if not
        """
        display_options = [0, 1, 2, 3, 4, 5, 6, 7]
        return self.command(address, 
            value = display_type,
            message = 'display type', 
            options = {str(v): v for v in display_options})


        # if display_type in display_options:
        #     return self.command(address, display_type, message='Setting display type')
        # else:
        #     logger.info('Incorrect argument for variable "display_type". Must be one of {}'.format(
        #         display_options))

    def heating_rate(self, heat_rate=None, address=35, decimals=1):
        """If heat_rate is specified, this method sets the heating rate of the furnace.
        If no argument is passed it queries the current heating rate
        :param heat_rate: heating rate in °C/min
        :type heat_rate: float, int
        :Example:
        >>> lab.furnace.heating_rate()
        10.0
        >>> lab.furnace.heating_rate(5)
        True
        >>> lab.furnace.heating_rate()
        5.0
        """
        return self.command(address, 
            value = heat_rate,
            message = 'heating rate',
            decimals=decimals)

    def indicated(self, address=1):
        """[Query only] Queries the current temperature of furnace.
        :returns: Temperature in °C if succesful, else False
        """
        return self.command(address, message='setpoint 1')

    def reset_timer(self):
        """Resets the current timer and immediately restarts. Used in for loops to reset the timer during every iteration. This is a safety measure should the program lose communication with the furnace.
        """
        if self.timer_status('reset'):
            return self.timer_status('run')

    def setpoint_1(self, temperature=None, address=24):
        """If temperature is specified, this method sets the target temperature of setpoint 1. If no argument is passed it queries the current target of setpoint 1.
        :param temperature: temperature in °C
        :type temperature: float, int
        :Example:
        >>> lab.furnace.setpoint_1()
        350.0
        >>> lab.furnace.setpoint_1(400)
        True
        >>> lab.furnace.setpoint_1()
        400
        """
        return self.command(address, temperature, message='setpoint 1')

    def setpoint_2(self, temperature=None, address=25):
        """If temperature is specified, this method sets the target temperature of setpoint 2. If no argument is passed it queries the current target of setpoint 2.
        .. note::
           Setpoint 2 is used as a 'safe' temperature for the furnace to reset to should something go wrong and communication is lost during high temperature experiments. The value is set during configuration of the instrument from the value RESET_TEMPERATURE in the config file. It is suggeseted to adjust the config file if a change is required rather than call this method directly.
        :param temperature: temperature in °C
        :type temperature: float, int
        :Example:
        >>> lab.furnace.setpoint_2()
        40.0
        >>> lab.furnace.setpoint_2(25.0)
        True
        >>> lab.furnace.setpoint_2()
        25.0
        """
        return self.command(address, temperature, message='setpoint 2')

    def remote_setpoint(self, temperature=None):
        """If temperature is specified, this method sets the target temperature of the remote setpoint. 
        :param temperature: temperature in °C
        :type temperature: float, int
        """
        return self.command(modbus_address=26, value=temperature, message='remote setpoint')

    def setpoint_select(self, selection=None, address=15):
        """If selection is specified, selects the current working setpoint. If no argument is passed, it returns the current working setpoint.
        options:
            'setpoint_1'
            'setpoint_2'
        :param selection: desired working setpoint
        :type selection: str
        """
        return self.command(address, 
            value = selection,
            message = 'current setpoint', 
            options = {'setpoint_1': 0, 'setpoint_2': 1})

    def timer_duration(self, hours=0, minutes=0, seconds=0, address=324):
        """Sets the length of the timer.
        :param minutes: number of minutes
        :type timer_type: int,float
        :param seconds: number of seconds
        :type timer_type: int,float (floats internally converted to int)
        """
        td = timedelta(hours=hours, minutes=minutes, seconds=seconds)
        if td.total_seconds() >= 100*60:
            self.timer_resolution('H:M')
            value = td.total_seconds()/60
        else:
            self.timer_resolution('M:S')
            value = td.total_seconds()

        return self.command(address, 
            value = value,
            message = 'timer duration',)

    def timer_end_type(self, selection=None, address=328):
        """Determines the behavior of the timer. The default configuration in this program is to dwell. If selection is specified, the timer end type will be set accordingly. If no argument is passed, it returns the current end type of the timer.
        .. note::
            This method is only valid if the timer type is set to 'dwell'
        options:
            'off'       : do nothing
            'current'   : dwell at the current setpoint
            'transfer' : transfer to setpoint 2 and dwell
        :param selection: desired type
        :type selection: str
        :Example:
        >>> lab.furnace.timer_type()    #five minutes
        'off'
        >>> lab.furnace.timer_type('dwell')
        True
        >>> lab.furnace.timer_type()
        'dwell'
        """
        return self.command(address, 
            value = selection,
            message = 'timer end type', 
            options = {'off': 0, 'current': 1, 'transfer': 2})

    def timer_resolution(self, selection=None, address=320):
        """Determines whether the timer display is in Hours:Mins or Mins:Seconds
        options:
            'H:M'   : Hours:Minutes
            'M:S'   : Minutes:Seconds
        :param selection: desired configuration
        :type selection: str
        """
        return self.command(address, 
            value = selection,
            message = 'timer resolution', 
            options = {'H:M': 0, 'M:S': 1})

    def timer_status(self, status=None, address=23):
        """Controls the furnace timer. If status is specified, the timer status will be set accordingly. If no argument is passed, it returns the current status of the timer.
        options:
            'reset' : resets the timer back to zero
            'run'   : starts the timer
            'hold'  : stops the timer
        :param status: desired working setpoint
        :type status: str
        :Example:
        >>> lab.furnace.timer_duration(minutes=5)    #five minutes
        True
        >>> lab.furnace.timer_status()
        'reset'
        >>> lab.furnace.timer_status('run')
        True
        >>> lab.furnace.setpoint_1()
        400
        """
        return self.command(address, 
            value = status,
            message = 'timer status', 
            options = {'reset': 0, 'run': 1, 'hold': 2})

    def timer_type(self, selection=None, address=320):
        """Determines the behavior of the timer. The default configuration in this program is to dwell. If status is specified, the timer status will be set accordingly. If no argument is passed, it returns the current status of the timer.
        options:
            'off'       : no timer
            'dwell'     : dwell at a fixed temperature until the timer runs out
            'delay'     : delayed start time
            'soft_start': start a process at reduced power
        :param selection: desired type
        :type selection: str
        :Example:
        >>> lab.furnace.timer_type()    #five minutes
        'off'
        >>> lab.furnace.timer_type('dwell')
        True
        >>> lab.furnace.timer_type()
        'dwell'
        """
        return self.command(address, 
            value = selection,
            message = 'timer type', 
            options = {'off': 0, 'dwell': 1, 'delay': 2, 'soft_start': 3})

    def flush_input(self):
        print('Flushing furnace input')
        self.serial.reset_input_buffer()

    def flush_output(self):
        print('Flushing furnace output')
        self.serial.reset_output_buffer()

    def shutdown(self):
        self.setpoint_1(20)
        self.timer_status('reset')

    def reconnect(self):
        self.__init__()

    
    def command(self, modbus_address, value=None, options={}, message='', decimals=0):
        '''Set or read value at specified modbus address.
        :param modbus_address: see furnace manual for adresses
        :type modbus_address: float, int
        :param value: value to be sent to the furnace
        :type value: float, int
        If a value is supplied it will return True if the command was succesful. If a value is not supplied, it will return the output of the instrument at specified modbus address.
        '''
        if value is not None:
            # print(modbus_address, options.get(value,value), decimals)
            print('Setting {} of furnace.'.format(message))
            self.write_register(modbus_address, options.get(value,value), number_of_decimals=decimals)
            return True
        else:
            #print('Getting {} from furnace.'.format(message))
            output = self.read_register(modbus_address, number_of_decimals=decimals)
            for k, v in options.items():
                if v == output:
                    return k
            return output


def get_ports():
    '''Returns a list of available serial ports for connecting to the furnace and stage
    :returns: list of available ports
    :rtype: list, str
    '''
    return {comport.manufacturer: comport.device for comport in list_ports.comports()}


def connect():
    # return LCR(), DAQ(), GasControllers(), Furnace()
    return Furnace()


def reconnect(lab_obj):

    # ports = get_ports()

    # if not ports: return
   
    if not lab_obj.furnace.status:
        lab_obj.furnace = Furnace()
   
    else:
        print('Thermocontroller is connected!')


#connect()