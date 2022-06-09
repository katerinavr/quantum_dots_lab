import time
import serial
import serial.tools.list_ports
import sys
import glob
import minimalmodbus
from minimalmodbus import Instrument

def main(): 
    # Serial port parameters    
    port = "COM8"
    slaveNumber = 1
    BAUDRATE = 9600
    STOPBITS = 1
    PARITY = "E"
    BYTESIZE = 8
    motka = Instrument(port, slaveNumber, debug=True)
    motka.serial.baudrate = BAUDRATE
    motka.serial.stopbits = STOPBITS
    motka.serial.parity = PARITY
    motka.serial.bytesize = BYTESIZE  
    motka.write_register(12, 231)        
    
    #Read data from device and write it to log file    
    #print ("Logger started. If you want to stop press Cntrl+C ") 
    #motka.write_register(12,  231)#, number_of_decimals=1)
    #try:
    #motka.read_register(3, 1)
    
    #data = []        
    #for value in registers.values():
    #    data.append( motka.read_register(value) )    
            #writeData(logFile, data)
    #except KeyboardInterrupt:
    #    print ("Logger was stopped by keyboard interrupt")
    #except:
    #    print('tza')
        #logFile.close()
        #motka.close()         
        #raise
    
    #logFile.close()
    #motka.close()
def sendCommand(self, command):
    try:
        arg = bytes(str(command), 'utf8') + b'\r'
        self.ser.write(arg)
        time.sleep(0.5)
        response = self.getResponse()
        return response
    except TypeError as e:
        if self.verbose:
            print(e)
        self.ser.close()
    
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
            print('Getting {} from furnace.'.format(message))
            output = self.read_register(modbus_address, number_of_decimals=decimals)
            for k, v in options.items():
                if v == output:
                    return k
            return output

main()