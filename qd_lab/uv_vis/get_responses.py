from scipy.interpolate import splrep, sproot, splev
from scipy.signal import find_peaks

class MultiplePeaks(Exception): pass
class NoPeaksFound(Exception): pass

def fwhm(x, y, k=10):
    """
    Determine full-with-half-maximum of a peaked set of points, x and y.

    Assumes that there is only one peak present in the datasset.  The function
    uses a spline interpolation of order k.
    """

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

def PL_max_intensity(reference_data, sample_refractive_index, sample_absorptrion, sample_emission):
    reference_QY = reference_data.QY
    reference_abs = reference_data.absorption
    reference_I = reference_data.emission
    reference_refractive_index = 1

    sample_QY = reference_QY*reference_abs*reference_I*(sample_refractive_index/reference_refractive_index)^2
    return sample_QY

def abs_max_intensity(dataset, range):
    """
    For a given Absorption spectra detect the maximum peak in a given range
    
    Args:
        dataset : The saved absorption spectra
        range: The range in nm, in which we expect the absorption peak for our material
    """
    intensities =dataset.intensities
    peaks, properties = find_peaks(intensities[range], height=0)
    return properties['peak_heights'].max()
