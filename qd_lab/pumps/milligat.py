import time
import serial
import serial.tools.list_ports
import sys
import glob
import minimalmodbus
#import serial
#ser = serial.Serial('COM8',9600)
#msg=f'CSL = 0\r\n'.encode()     
#ser.write(msg)

#msg=f'CSL = 46200\r\n'.encode()
# ser.write(msg)
#connection = Connection(port='COM8', baudrate=9600) 
#connection.openConnection 
# ser = serial.Serial('COM8',9600)
#ser.write("AVM 46208\r".encode())
#serial.timeout = 0.2
#comm = ser.readlines()
#ser.flush()
#462

PUMP_ADDRESS = 'COM8'
#ser.write("%01#RDD0010000107**\r".encode())
class Connection(object):
    def __init__(self, port, baudrate=9600, x = 0, mode = 0, verbose=False):
        self.port = port
        self.baudrate = baudrate
        #self.x = x
        #self.mode = mode
        self.verbose = verbose

    def openConnection(self):
  
        try:
            self.ser = serial.Serial()
            self.ser.baudrate = self.baudrate
            self.ser.port = self.port
            self.ser.timeout = 0
            self.ser.open()
            if self.ser.isOpen():
                print('open')
                if self.verbose:
                    print("Opened port")
                    print(self.ser)
                #self.getPumpStatus()
                #self.ser.flushInput()
                #self.ser.flushOutput()
        except Exception as e:
            if self.verbose:
                print('Failed to connect to pump')
                print(e)
            #pass

    def closeConnection(self):
        self.ser.close()
        if self.verbose:
            print("Closed connection")

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

    def getResponse(self):
        try:
            response_list = []
            while True:
                response = self.ser.readlines()
                #print('tza', response)
                for line in response:
                    line = line.strip(b'\n').decode('utf8')
                    line = line.strip('\r')
                    if self.verbose:
                        print(line)
                    response_list.append(line)
                break
            return response_list
        except TypeError as e:
            if self.verbose:
                print(e)
            self.closeConnection()
        except Exception as f:
            if self.verbose:
                print(f)
            self.closeConnection()

    def startPump(self):
        command = 'start'
        #command = self.addX(command)
        #command = self.addMode(command)
        response = self.sendCommand(command)
        return response

    def stopPump(self):
        command = 'SSTP'
        command = self.addX(command)
        response = self.sendCommand(command)
        return response

    def pausePump(self):
        command = 'pause'
        command = self.addX(command)
        response = self.sendCommand(command)
        return response

    def restartPump(self):
        command = 'restart'
        response = self.sendCommand(command)
        return response

    def setUnits(self, units):
        units_dict = {'mL/min': '0', 'mL/hr': '1', 'μL/min': '2', 'μL/hr': 3}
        command = 'set units ' + str(units_dict[units])
        response = self.sendCommand(command)
        return response

    def setDiameter(self, diameter):
        command = 'set diameter ' + str(diameter)
        response = self.sendCommand(command)
        return response

    def setRate(self, rate):
        command = 'VM ' + str(rate)
        response = self.sendCommand(command)
        return response

    def setVolume(self, volume):
        command = 'set volume ' + str(volume)
        response = self.sendCommand(command)
        return response

    def setDelay(self, delay):
        command = 'set delay ' + str(delay)
        response = self.sendCommand(command)
        return response

    def setTime(self, timer):
        command = 'set time ' + str(timer)
        response = self.sendCommand(command)
        return response

    def getParameterLimits(self):
        command = 'read limit parameter'
        response = self.sendCommand(command)
        return response

    def getParameters(self):
        command = 'view parameter'
        response = self.sendCommand(command)
        return response

    def getDisplacedVolume(self):
        command = 'dispensed volume'
        response = self.sendCommand(command)
        return response

    def getElapsedTime(self):
        command = 'elapsed time'
        response = self.sendCommand(command)
        return response

    def getPumpStatus(self):
        command = 'pump status'
        response = self.sendCommand(command)
        return response
        
def connect():
        # return LCR(), DAQ(), GasControllers(), Furnace()
    return Connection()