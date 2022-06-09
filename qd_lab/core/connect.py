import time
import serial
import serial.tools.list_ports
import sys
import glob

def getOpenPorts():
    # portinfo = []
    # for port in serial.tools.list_ports.comports():
    #     if port[2] != 'n/a':
    #         info = [port.device, port.name, port.description, port.hwid]
    #         portinfo.append(info)
    # return portinfo

    if sys.platform.startswith('win'):
        ports = ['COM%s' % (i + 1) for i in range(256)]
    elif sys.platform.startswith('linux') or sys.platform.startswith('cygwin'):
        # this excludes your current terminal "/dev/tty"
        ports = glob.glob('/dev/tty[A-Za-z]*')
    elif sys.platform.startswith('darwin'):
        ports = glob.glob('/dev/tty.*')
    else:
        raise EnvironmentError('Unsupported platform')
    result = []
    for port in ports:
        try:
            s = serial.Serial(port)
            s.close()
            result.append(port)
            #print(port)
        except (OSError, serial.SerialException):
            pass
    #print(result)
    return result

def parsePortName(portinfo):
    """
    On macOS and Linux, selects only usbserial options and parses the 8 character serial number.
    """
    portlist = []
    for port in portinfo:
        if sys.platform.startswith('win'):
            portlist.append(port[0])
        elif sys.platform.startswith('darwin') or sys.platform.startswith('linux'):
            if 'usbserial' in port[0]:
                namelist = port[0].split('-')
                portlist.append(namelist[-1])
    return portlist

class Connection(object):
    def __init__(self, port, baudrate, x = 0, mode = 0, verbose=False):
        self.port = port
        self.baudrate = baudrate
        self.x = x
        self.mode = mode
        self.verbose = verbose

    def openConnection(self):
        try:
            self.ser = serial.Serial()
            self.ser.baudrate = self.baudrate
            self.ser.port = self.port
            self.ser.timeout = 0
            self.ser.open()
            if self.ser.isOpen():
                if self.verbose:
                    print("Opened port")
                    print(self.ser)
                self.getPumpStatus()
                self.ser.flushInput()
                self.ser.flushOutput()
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
        command = self.addX(command)
        command = self.addMode(command)
        response = self.sendCommand(command)
        return response

    def stopPump(self):
        command = 'stop'
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
        command = 'set rate ' + str(rate)
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
        
    def addMode(self, command):
        if self.mode == 0:
            return command
        else:
            return command + ' ' + str(self.mode - 1)

    def addX(self, command):
        if self.x == 0:
            return command
        else:
            return str(self.x) + ' ' + command