import streamlit as st
import pandas as pd
import numpy as np
import base64
import os, urllib
from utils.get_plots import *

st.title('Setting the Quantum Dots lab')
col1, col2, col3 = st.columns([1, 1, 1])


with col1:   
    st.selectbox('Select the lab components',  ['Chemyx', 'Milligat_A', 'Milligat_B', 'Milligat_C', 'Thermocontroller'])
    st.selectbox("",['Chemyx', 'Milligat_A', 'Milligat_B', 'Milligat_C', 'Thermocontroller'],  key=0)
    st.selectbox("", ['Chemyx', 'Milligat_A', 'Milligat_B', 'Milligat_C', 'Thermocontroller'], key=1)

with col2:
    st.text_input('Enter the COM channel') 
    st.text_input("", key=2)
    st.text_input("",  key=3)

with col3:
    st.text_input('Parameters: [min, max, step]')
    st.text_input("", key=4)
    st.text_input("", key=5)


col4, col5, col6 = st.columns([1, 1, 1])

with col4:   
    st.selectbox('Select the analytical equipment',  ['Absorption_Spectrometer', 'Emission_Spectrometer'], key=6)
    st.selectbox("",  ['Absorption_Spectrometer', 'Emission_Spectrometer'], key = 7)

with col5:
    st.text_input('Enter the COM channel', key=7) 
    st.text_input("", key=8)


st.title('Responces')
col7, col8, col9 = st.columns([1, 1, 1])

with col7:
    #st.markdown('Temperature VS time')
    fig1 = temperature_vs_time()
    st.pyplot(fig1)
    #st.image(fig)# call the plot funtion

with col8:
    #st.title('Pump rates VS time')
    fig2 = pump_rate_vs_time()
    st.pyplot(fig2)

with col9:
    #st.title('UV-VIS spectra')
    fig3 = UV_VIS()
    st.pyplot(fig3)

col10, col11, col12 = st.columns([1, 1, 1])

with col10:
    st.markdown('Quantum Yield')
    # call the plot funtion

with col11:
    st.markdown('FWHM')
    #FWHM(df)


st.sidebar.markdown("## Select the Optimization Strategy")
optimizer = st.sidebar.selectbox('Select optimizer',
                                    ['TSEMO', 'MVMOO']) 
  
if st.sidebar.button('Start the autonomous experiment'):
    # with click write these parameters in the config file and run the lab manager
    st.write('test')

# plot the response surface in 3D by user defined x,y,z in side bar
