# Overview
Code for setting up a fully automonous process in flow for the production on Quantum Dots of different sizes.
Our equipment includes:
- Milligat pumps
- Chemyx pumps
- Thermocontroller (Eurotherm)
- Ocean optics UV-Vis spectrometers 

# Installation
1. Install python (version 3 or above)
2. Create a conda environment
```
conda create --name qd_lab
conda activate qd_lab
```
3. Clone this repository:
```git clone https://github.com/katerinavr/quantum_dots_lab.git ```
4. Install the libraries
```pip install -r requirements.txt```

# Examples

Setting the Milligat pump:
```
import serial

ser8 = serial.Serial('COM8',9600)
msg=f'ASL = {flow rate}\r\n'.encode()
ser10.write(msg)
```

Running an experiment using the current settings:

```
python qd_lab/lab.py -pump_rate_A <pump_rate_A> -pump_rate_B <pump_rate_B> -pump_rate_C <pump_rate_C> -temperature <temperature> -optimizer <select_optimizer>
```