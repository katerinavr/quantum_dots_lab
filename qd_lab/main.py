from random import choices
from secrets import choice
from shutil import register_unpack_format
import sys
import os
from pumps import chemyx
from pumps.chemyx import *
import argparse
import time

#connection = connect.Connection(port_number, baudrate, x = 0, mode = 0, verbose=False)
# python main.py --port_number 'COM4' --baudrate 9600 --x 0

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    #parser.add_argument('--list_port', default= False, action= 'store_true')
    #parser.add_argument('--port_number', type = str)
    parser.add_argument('--baudrate', type = str, choices=['9600', '38400'])
    parser.add_argument('--x',type = str)
    #parser.add_argument('--mode',type = str)
    #parser.add_argument('--verbose', default= False, action= 'store_true' )
    parser.add_argument('--rate', type = int )
   
    args = parser.parse_args()
    #print(args.port_number)
    #if args.list_port:
    #    print(connect.getOpenPorts())
    #    return

    connection = chemyx.Connection('COM4', baudrate=9600, x = 0, mode = 0, verbose=False)
    #connect.Connection('COM4', baudrate = args.baudrate,  x = args.x,  mode=0, verbose=False)
    connection.openConnection()

    print("Starting the Pump")
    connection.startPump()
    connection.setUnits('mL/min')
    connection.setRate(args.rate)
    time.sleep(5)
    # Stop the pump and close the connection
    connection.stopPump()
    connection.closeConnection()

if __name__ == "__main__":
    main()