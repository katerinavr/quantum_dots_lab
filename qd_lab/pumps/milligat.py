import serial

class Milligat:

    def __init__(self, name, ser):
        """ Creates a controller for the MilliGat pumps

        Args:
            name: The name of the pump being controlled. This should be either 'A', 'B' or 'C'.
            ser: The serial connection used to communicate with the pump. See pyserial for more information.
        """
        self.name = name
        self.ser = ser
        #try:
        #   ser.open()
        #except:pass
    
    def set_flow_rate(self, flow_rate):
        msg = f'{self.name}SL = {flow_rate}\r\n'.encode()
        self.ser.write(msg)

    def stop_pump(self):
        self.set_flow_rate(flow_rate=0)


