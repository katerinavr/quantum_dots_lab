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

## Unit tests
```
python -m pytest
```

# Examples

Setting the Milligat pump:
```
from qd_labs.pumps import milligat

pump_c = milligat.Milligat('C', serial.Serial('COM8', 9600))
pump_c.set_flow_rate(1000)
pump_c.stop_pump()
```

Measure Residense Time distribution (RTD):

```
python qd_lab/uv_vis/measure_rtd.py
```

Running an experiment using the current settings:

```
python qd_lab/lab.py config.json
```