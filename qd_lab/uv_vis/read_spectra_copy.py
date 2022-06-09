from typing import Any
import seabreeze
seabreeze.use('cseabreeze')
from seabreeze.spectrometers import Spectrometer
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from specutils.manipulation import median_smooth
from specutils import Spectrum1D
import astropy.units as u
from specutils.manipulation import (box_smooth, gaussian_smooth, trapezoid_smooth)
from scipy.signal import find_peaks
import threading
import time
from datetime import datetime, timedelta

def printit():
  threading.Timer(5.0, printit).start()
  max_absorption = properties['peak_heights'].max()
  print(max_absorption)
  with open("src/uv_vis/absorption_log.txt", "a") as file_object:
        file_object.write(str(datetime.now()) + ' ' + str(max_absorption))
        file_object.write('\n')


# add def for the functions and arguments for saving data
fiber_only = pd.read_csv('src/uv_vis/background.csv')
fiber_intensity = fiber_only.intensities

solvent_only = pd.read_csv('src/uv_vis/ethanol_nobackground.csv')

# Equivalent to scans to average functionality

wavelengths = solvent_only.wavelength.values #spec.wavelengths()
intensities = solvent_only.intensities.values #spec.intensities(correct_nonlinearity=True,correct_dark_counts = True)


spec = Spectrum1D(spectral_axis=wavelengths* u.Unit('nm'), flux=intensities* u.Unit('A') ) # [wavelengths, intensities]
spec_bsmooth = box_smooth(spec, width=20).flux
intensities = spec_bsmooth  #intensities #- fiber_intensity

#dataset=pd.concat([pd.DataFrame(wavelengths, columns=['wavelength']),
#pd.DataFrame(intensities, columns=['intensities'])], axis=1)
#dataset.to_csv('src/uv_vis/ethanol_nobackground.csv', index=None)  

plt.plot(intensities)
plt.xlabel('wavelengths')
plt.ylabel('intensities')
plt.xlim(300, 900)
peaks, properties = find_peaks(intensities[400:800], height=0)

plt.plot(peaks+400, intensities[peaks+400], "x")
print(properties['peak_heights'].max())

plt.show()
#printit()
#except ValueError: 
#    printit_zero()




# def read_absorption(compchannel of spectrometer1) 
# def read_emission(compchannel of spectrometer2)