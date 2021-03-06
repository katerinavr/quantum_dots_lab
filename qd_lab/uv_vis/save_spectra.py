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

# Connent the spectrometer for absorption
spec1 = Spectrometer.from_serial_number('USB2+H05739')
#Spectrometer.from_serial_number('FLMS16051')
#spec1 = Spectrometer.from_first_available()
spec1.integration_time_micros(300000)
#print(spec1)

# Connent the spectrometer for emmision
#spec2 = Spectrometer.from_serial_number('FLMS16051')#('USB2+H05739')
#spec2.integration_time_micros(6000000)

def printit():
  """Record the absorption peak over time"""
  threading.Timer(5.0, printit).start()
  max_absorption = get_absorption() 
  #print(max_absorption)
  with open("src/uv_vis/absorption_log.txt", "a") as file_object:
        file_object.write(str(datetime.now()) + ' ' + str(max_absorption))
        file_object.write('\n')

def get_absorption():
    """Get the maximum absorption peak at a certain wavelength"""
    fig = plt.figure()
    fiber_only = pd.read_csv('C:/Users/kvriz/Dropbox/Leeds_Sheffield/uv_vis_spectra/background_spectra/black_DT.csv')
    fiber_intensity = fiber_only.intensities
    solvent_only = pd.read_csv('C:/Users/kvriz/Dropbox/Leeds_Sheffield/uv_vis_spectra/background_spectra/water_DT.csv')
    # Equivalent to scans to average functionality
    wavelngt=[]
    inte=[]
    for i in range(5):
	    inte.append(spec1.intensities(correct_nonlinearity=True,correct_dark_counts = True)- fiber_intensity)
	    wavelngt.append(spec1.wavelengths())
    wavelengths = np.mean(wavelngt, axis=0) #spec.wavelengths()
    intensities = np.mean(inte, axis=0) #spec.intensities(correct_nonlinearity=True,correct_dark_counts = True)
    
    intensities= -np.log10(intensities/solvent_only.intensities)
    intensities = np.nan_to_num(intensities.values, nan=0, neginf=0)

    spec = Spectrum1D(spectral_axis=wavelengths* u.Unit('nm'), flux=intensities* u.Unit('A') )
    spec_bsmooth = box_smooth(spec, width=10).flux
    intensities = spec_bsmooth  #intensities #- fiber_intensity
    
    dataset=pd.concat([pd.DataFrame(wavelengths, columns=['wavelength']),
    pd.DataFrame(intensities, columns=['intensities'])], axis=1)
    
    #dataset.to_csv('C:/Users/kvriz/Dropbox/Leeds_Sheffield/uv_vis_spectra/background_spectra/black_DT.csv')
    #dataset.to_csv('C:/Users/kvriz/Dropbox/Leeds_Sheffield/uv_vis_spectra/background_spectra/water_DT.csv', index=None)
    
    #return dataset
    #('qd_lab/data/uv_vis_plots/qd_experiment_1/Abs_KV1_10_180_1.csv', index=None)
    #max_red = dataset.intensities.values[450:600].max()
    #print(max_red)
    #max_blue = dataset.intensities.values[935:1700].max()
    #print(max_blue)
    #diff = abs(max_red -max_blue)
    #print(diff)
    return dataset
    #plt.plot(wavelengths,intensities)
    #plt.xlabel('wavelengths')
    #plt.ylabel('intensities')

    #plt.xlim(200, 1000)
    #return fig
    #peaks, properties = find_peaks(intensities[400:800], height=0)
    #plt.plot(peaks+400, intensities[peaks+600], "x")
    #print(properties['peak_heights'].max())
    #print(properties['peak_heights'].remove(properties['peak_heights'].max()))
    #plt.show()
    
    #return properties['peak_heights'].max()

def get_emmision():
    """Get the maximum emmision peak at a certain wavelength"""
    fiber_only = pd.read_csv('qd_lab/data/uv_vis_plots/default_spectra/emmision_background_dh.csv')
    fiber_intensity = fiber_only.intensities
    fig = plt.figure()
    # Equivalent to scans to average functionality
    wavelngt=[]
    inte=[]
    for i in range(8):
	    inte.append(spec2.intensities(correct_nonlinearity=True,correct_dark_counts = True) )#- fiber_intensity)
	    wavelngt.append(spec2.wavelengths())
    wavelengths = np.mean(wavelngt, axis=0) 
    intensities = np.mean(inte, axis=0)
    spec = Spectrum1D(spectral_axis=wavelengths* u.Unit('nm'), flux=intensities* u.Unit('A') )
    spec_bsmooth = box_smooth(spec, width=60).flux
    intensities = spec_bsmooth 

    dataset=pd.concat([pd.DataFrame(wavelengths, columns=['wavelength']),
    pd.DataFrame(intensities, columns=['intensities'])], axis=1)
    dataset.to_csv('qd_lab/data/uv_vis_plots/qd_experiment_1/PL_batcg_KV1_5_180_test.csv', index=None)
    plt.plot(wavelengths,intensities)
    plt.xlabel('wavelengths')
    plt.ylabel('intensities')
    #plt.ylim(0, 500)
    plt.xlim(200, 900)
    plt.show()
    #
    
    #peaks, properties = find_peaks(intensities[600:800], height=0)
    #plt.plot(peaks+600, intensities[peaks+600], "x")
    #print(properties['peak_heights'].max())
    #return plt.show()
    #return properties['peak_heights'].max()
    #return fig

#printit()
#get_absorption()
#get_emmision()