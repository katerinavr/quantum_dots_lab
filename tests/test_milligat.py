from qd_lab.pumps import milligat

class FakeSerial:
    def __init__(self, **kwargs):
        self.write_buffer = []
    
    def write(self, string):
        self.write_buffer.append(string)

def test_milligat_init():
    pump = milligat.Milligat('A', FakeSerial())
    assert pump.name == 'A'

def test_set_flowrate():
    ser = FakeSerial()
    pump = milligat.Milligat('A', ser)
    pump.set_flow_rate(1600)
    assert len(ser.write_buffer) == 1
    assert ser.write_buffer == [b'ASL = 1600\r\n']

def test_stop_flowrate():
    ser = FakeSerial()
    pump = milligat.Milligat('A', ser)
    pump.stop_pump()
    assert len(ser.write_buffer) == 1
    assert ser.write_buffer == [b'ASL = 0\r\n']

def test_flowrate_update():
    ser = FakeSerial()
    pump = milligat.Milligat('A', ser)
    pump.set_flow_rate(1600)
    # Updating the flow rate after sometime
    pump.set_flow_rate(2600)
    # Stopping the pump
    pump.stop_pump()
    assert len(ser.write_buffer) == 3
    assert ser.write_buffer == [b'ASL = 1600\r\n', b'ASL = 2600\r\n', b'ASL = 0\r\n']