import seabreeze.spectrometers as sb
import numpy as np
import pandas as pd
import datetime
from scipy.interpolate import splrep, sproot, splev
from scipy.signal import find_peaks
import numpy as np

class MultiplePeaks(Exception): pass
class NoPeaksFound(Exception): pass

#Note to self: Make the buffer a list of dictionaries each with the stage position and spectraself.
#Use pop(0) to pop off the first spectra in the buffer when get_spectrum is called
class OceanOptics(object):
    """Class to define the spectrometers
    Attributes:
        spectrometer_model (str): Model of the spectrometer (e.g., FLMS02673)
        seabreeze (:obj:): Seabreeze.spectrometers object
    """
    def __init__(self, spectrometer_model, seabreeze):
        self.spectrometer_model = spectrometer_model # Spectrometer model number
        self.seabreeze = seabreeze
        self.spectrometer_on = False # Initialize the spectrometer to off
        # Initialize wavelengths_splice, normalized_absorbance, and fluorescence to empty
        self.blank_intensities = []
        self.dark_intensities = []
        self.buffer = []

        #Check that the spectrometer is connected 
        try:
            self.ocean_optics = self.seabreeze.Spectrometer.from_serial_number(self.spectrometer_model)
            self.ocean_optics.close()
        except Exception:
            raise IOError("Spectrometer not connected")

    def __enter__(self):
        ## Initialize self.ocean_optics to be a spectrometer from seabreeze package
        try:
            self.ocean_optics = self.seabreeze.Spectrometer.from_serial_number(self.spectrometer_model)
            self.spectrometer_on = True
            return self
        except Exception:
            raise IOError("Spectrometer not connected")
    
    def __exit__(self, *args):
        #Close the spectrometer object on exit
        try:
            self.ocean_optics.close()
        except Exception:
            pass
        
    def read_spectrometer_raw(self, integration_time):
        """Function to print the raw data from the spectreomter
        Args:
            integration_time (float): Integration time in microseconds
        Yields:
            Numpy matrix with first column as wavelengths and second column a intensisties
        """
        # if not self.spectrometer_on:
        #     raise NameError("Spectrometer not connected")

        # Setting the integration time into the spectrometer and integrating
        self.ocean_optics.integration_time_micros(integration_time)
        # Assigning wavelength values into wavelengths
        wavelengths = self.ocean_optics.wavelengths()
        # Assigns intensity into intensities array
        intensities = self.ocean_optics.intensities(correct_dark_counts=True, correct_nonlinearity=True)
        #Return spectrum array with wavelengths and intensities
        spectrum = [wavelengths, intensities]
        output = [[],[]]
        #Convert int64 to int
        for i, column in enumerate(spectrum):
            for value in column:
                try:
                    output[i].append(float(value))             
                except AttributeError:
                    pass
                except TypeError:
                    pass
        return output
        

    def store_blank(self, blank):
        """ Method to save blank intensisties
        Args:
            blank (array): Two column array of wavelengths and intesities
        """
        if isinstance(blank, list):
            #assuming it a two column array of wavelengths and intensities
            self.blank_intensities = blank[1]
        else:
            raise ValueError('Please pass an array of wavelengths and intensities')

    def store_dark(self, dark):
        """ Method to save dark intensisties
        Args:
            dark (array): Two column array of wavelengths and intesities
        """
        if isinstance(dark, list):
            #assuming it a two column array of wavelengths and intensities
            self.dark_intensities = dark[1]
        else:
            raise ValueError('Please pass a list of wavelengths and intensities')

    def absorbance_read(self, integration_time, scans_to_average, filter=0, normalized=False):
        """
        Function to read the UV data from the spectrometer
        Stores the normalized absorbance and flourescence data into Spectrometer Object
        Args:
            integration_time (float): Integration time in microseconds
            scans_to_average (int): Number of scans to average over
            filter (int, optional): The starting point for the Spectrum (e.g, start from the 300th data point). Defaults to use the whole spectram
            normalize (bool): If true, absorbances will be normalized to the maximum absorbance.  Defaults to false.
        Yields:
            Numpy array with first column as wavelengths and second column as absorbance
            
        """
        #check types
        if not isinstance(scans_to_average, int):
            raise ValueError('Please pass an integer number of scans to average')
        if not isinstance(filter, int):
            raise ValueError('Please pass an integer number for filter')

        #Make sure dark and blanks exist
        if len(self.dark_intensities) == 0: raise ValueError("Please save dark values")
        if len(self.blank_intensities) == 0: raise ValueError("Please save blank values")

        # If the spectrometer is on
        if not self.spectrometer_on:
            raise NameError("Spectrometer not connected")

        #Set integration time
        self.ocean_optics.integration_time_micros(integration_time)

        #Get wavelengths and drop useless data
        wavelengths = self.ocean_optics.wavelengths()
        wavelengths_splice = np.array(wavelengths[filter:])

        #Subtract dark from blank
        blank = np.array(self.blank_intensities[filter:])
        dark = np.array(self.dark_intensities[filter:])
        blank_minus_dark = np.subtract(blank, dark)

        #Find absorbance averaged over requested number of scans
        average_buffer = [[] for i in range(scans_to_average)]
        for i in range(scans_to_average):
            average_buffer[i] = self.ocean_optics.intensities(correct_dark_counts=True, correct_nonlinearity=True)
        average_intensities = np.mean(average_buffer, axis = 0) #average element wise the arrays
        intensities_splice = np.array(average_intensities[filter:])
        intensities_splice_minus_dark = np.subtract(intensities_splice, dark)
        absorbance = -np.log10(blank_minus_dark/intensities_splice_minus_dark)
        if normalized:
            maximum = np.amax(absorbance)
            absorbance = absorbance/maximum

        #Remove Nans
        absorbance = [x for x in absorbance if ~np.isnan(x)]

        #Return spectrum array with wavelengths and absorbances
        spectrum = [wavelengths_splice, intensities_splice]
    
        output = [[],[]]
        #Convert int64 to int
        for i, column in enumerate(spectrum):
            for value in column:
                try:
                    output[i].append(float(value))             
                except AttributeError:
                    pass
                except TypeError:
                    pass
        #return output
        # return the dataframe named according to the date/time it was produced
        name = f'abs_{datetime.datetime.now().strftime("%H%M_%m%d%Y")}.csv'
        dataset = pd.DataFrame(output, columns=['wavelenght, absorption']).
        dataset.to_csv('uv_vis/uv_vis_spectra/absorption/name')
        return dataset

    def fluorescence_read(self,integration_time, scans_to_average, filter=0):
        
        self.ocean_optics.integration_time_micros(integration_time)

        #Get wavelengths and drop useless data
        wavelengths = self.ocean_optics.wavelengths()
        wavelengths_splice = np.array(wavelengths[filter:])

        #Subtract dark from blank
        dark = np.array(self.dark_intensities[filter:])

        #Find absorbance averaged over requested number of scans
        average_buffer = [[] for i in range(scans_to_average)]
        for i in range(scans_to_average):
            average_buffer[i] = self.ocean_optics.intensities(correct_dark_counts=True, correct_nonlinearity=True)
        average_intensities = np.mean(average_buffer, axis = 0) #average element wise the arrays
        intensities_splice = np.array(average_intensities[filter:])
        intensities_splice_minus_dark = np.subtract(intensities_splice, dark)
        
        #Remove Nans
        absorbance = [x for x in absorbance if ~np.isnan(x)]

        #Return spectrum array with wavelengths and absorbances
        spectrum = [wavelengths_splice, intensities_splice_minus_dark]
    
        output = [[],[]]
        #Convert int64 to int
        for i, column in enumerate(spectrum):
            for value in column:
                try:
                    output[i].append(float(value))             
                except AttributeError:
                    pass
                except TypeError:
                    pass
        #return output
        # return the dataframe named according to the date/time it was produced
        name = f'emission_{datetime.datetime.now().strftime("%H%M_%m%d%Y")}.csv'
        dataset = pd.DataFrame(output, columns=['wavelenght, emission'])
        dataset.to_csv('uv_vis/uv_vis_spectra/absorption/name')
        return dataset

    def abs_max_intensity(self, dataset, range):
        """
        For a given Absorption spectra detect the maximum peak in a given range
        
        Args:
            dataset : The saved absorption spectra
            range: The range in nm, in which we expect the absorption peak for our material
        """
        dataset = self.absorbance_read
        intensities =dataset.intensities
        peaks, properties = find_peaks(intensities[range], height=0)
        return properties['peak_heights'].max()
    
    def fwhm(self, k=10): # add the range of emmission
        """
            Determine full-with-half-maximum of a peaked set of points, x and y.
            Assumes that there is only one peak present in the datasset.  The function
            uses a spline interpolation of order k.
        """
        dataset = self.fluorescence_read
        x= dataset.wavelenght
        y= dataset.emission
        half_max = np.amax(y)/2.0
        s = splrep(x, y - half_max, k=k)
        roots = sproot(s)

        if len(roots) > 2:
            raise MultiplePeaks("The dataset appears to have multiple peaks, and "
                    "thus the FWHM can't be determined.")
        elif len(roots) < 2:
            raise NoPeaksFound("No proper peaks were found in the data set; likely "
                        "the dataset is flat (e.g. all zeros).")
        else:
            return abs(roots[1] - roots[0])

    def PL_max_intensity(self, reference_data, sample_refractive_index, sample_absorptrion, sample_emission):
        
        reference_QY = reference_data.QY
        reference_abs = reference_data.absorption
        reference_I = reference_data.emission
        reference_refractive_index = 1
        absorption_dataset = self.absorbance_read
        emmision_dataset = self.fluorescence_read
        sample_QY = reference_QY*reference_abs*reference_I*(sample_refractive_index/reference_refractive_index)^2
        return sample_QY