import matplotlib.pyplot as plt
from scipy.stats import norm
import numpy as np
import math

#plt.rcParams["figure.figsize"] = (10,8)

def temperature_vs_time():
    plt.title('Temperature VS time')
    plt.plot([100, 150, 180, 200])
    plt.xlabel('Time')
    plt.ylabel('Temperature')
    #plt.show()
    #plot = plt.plot(df.time. df.temperature)
    return plt

def pump_rate_vs_time():
    plt.title('Pump rate VS time')
    plot = plt.plot([0.1, 0,3, 0.2, 0.6])
    plt.xlabel('Time')
    plt.ylabel('Pump rate (mL/min)')
    #plot = plt.plot(df.time. df.pump_rate)
    return plot

def UV_VIS():
    plt.title('UV_vis spectra')
    mu = 0
    variance = 1
    sigma = math.sqrt(variance)
    x = np.linspace(mu - 3*sigma, mu + 3*sigma, 100)
    plt.plot(x, stats.norm.pdf(x, mu, sigma))
    plt.xlabel('Time')
    plt.ylabel('Absorption')
    #plot = plt.plot(df.time. df.absorption)
    return plt

def quantum_yield(df):
    plot = plt.scatter(df.quantum_yield)
    return plot

def FWHM(df):
    plot = plt.scatter(df.FWHM)
    return plot