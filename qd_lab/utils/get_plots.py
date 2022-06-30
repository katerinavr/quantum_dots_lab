import matplotlib.pyplot as plt
from scipy.stats import norm
import scipy.stats as stats
import numpy as np
import pandas as pd
import math

#plt.rcParams["figure.figsize"] = (10,8)

def temperature_vs_time():
    fig = plt.figure()
    plt.title('Temperature VS time')
    plt.plot(np.ones(20)*25, marker='x', markerfacecolor = '#c20078', markeredgecolor='#c20078', linewidth=3, markeredgewidth=3, markersize=6)
    plt.xlabel('Time')
    plt.ylabel('Temperature')
    #plt.show()
    #plot = plt.plot(df.time. df.temperature)
    return fig

def pump_rate_vs_time():
    fig = plt.figure()
    plt.title('Pump rate VS time')
    plt.plot(np.ones(20)*2, marker='x', markerfacecolor = '#c20078', markeredgecolor='#c20078', linewidth=3, markeredgewidth=3, markersize=6)
    plt.xlabel('Time')
    plt.ylabel('Pump rate (mL/min)')
    plt.ylim(0,4)
    #plot = plt.plot(df.time. df.pump_rate)
    return fig

def Abs():
    fig = plt.figure()
    plt.title('Abs spectra')
    data = pd.read_csv('qd_lab/data/uv_vis_plots/red_food_absorption.csv')
    plt.plot(data.wavelength, data.intensity, linewidth=3) 
    plt.xlim(200, 800)
    plt.xlabel('Wavelength (nm)')
    plt.ylabel('Absorbance')
    return fig

def UV_VIS():
    import scipy.stats as stats
    fig = plt.figure()
    plt.title('PL spectra')
    h = [186, 176, 158, 180, 186, 168, 168, 164, 178, 170, 189, 195, 172,
     187, 180, 186, 185, 168, 179, 178, 183, 179, 170, 175, 186, 159,
     161, 178, 175, 185, 175, 162, 173, 172, 177, 175, 172, 177, 180]
    h.sort()
    hmean = np.mean(h)
    hstd = np.std(h)
    pdf = stats.norm.pdf(h, hmean, hstd)
    plt.plot(h, pdf,linewidth=3) 
    plt.xlabel('Wavelength (nm)')
    plt.ylabel('Emission')
    #plot = plt.plot(df.time. df.absorption)
    return fig

def PL_spectra():
    import scipy.stats as stats
    fig = plt.figure()
    plt.title('PL spectra')
    mu = 0
    variance = 1
    sigma = math.sqrt(variance)
    x = np.linspace(mu - 3*sigma, mu + 3*sigma, 100)
    fig = plt.plot(x, stats.norm.pdf(x, mu, sigma))
    plt.xlabel('Time')
    plt.ylabel('Emission')
    #plot = plt.plot(df.time. df.absorption)
    return fig    

def quantum_yield(df):
    plot = plt.scatter(df.quantum_yield)
    return plot

def FWHM(df):
    plot = plt.scatter(df.FWHM)
    return plot